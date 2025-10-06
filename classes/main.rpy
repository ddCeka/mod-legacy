
init python:
    class mod(NonPicklable):
        version = '0.5'
        scaleFactor = config.screen_height / 1080.0 
        gestureInitialized = False
        
        Settings = modSettingsClass()
        Loader = modLoader()
        Search = modSearchClass()
        Choices = modChoicesClass()
        PathDetection = modPathDetectionClass()
        TextBox = modTextBox()
        TextRepl = modTextReplacementsClass()
        Gamesaves = modGameSaves()
        LabelMon = modLabelMon()
        StoreMonitor = modStoreMonitor
        Notifications = modNotifications()
        Snapshots = modSnapshots()
        
        @staticmethod
        def init():
            mod.scaleFactor = config.screen_height / 1080.0
            mod.LabelMon.init()
            if not 's_e_n' in config.gestures:
                config.gestures['s_e_n'] = 'alt_K_m'
                mod.gestureInitialized = True
        
        @staticmethod
        def afterLoad(): 
            renpy.show_screen('mod_overlay')
            mod.StoreMonitor.init()
            mod.Loader.autoLoad()
        
        @staticmethod
        def onLabelCalled(label, called):
            if label == 'start':
                mod.afterLoad()
            elif label == '_start_replay':
                renpy.show_screen('mod_overlay')
        
        @staticmethod
        class Open(NonPicklable):
            def __call__(self):
                if _in_replay:
                    mod.Confirm("Do you want to end the current replay?", renpy.end_replay, title='End replay')()
                else:
                    renpy.take_screenshot()
                    renpy.run(Show('mod_main'))
        
        @staticmethod
        def scalePx(size):
            """ Change size from 1080p to game resolution """
            return size*mod.scaleFactor
        
        @staticmethod
        def scalePxInt(size):
            return int(mod.scalePx(size))
        
        @staticmethod
        def scale(percentage, size):
            return int((percentage / 100.0) * size)
        
        @staticmethod
        def scaleX(percentage):
            return mod.scale(percentage, config.screen_width)
        
        @staticmethod
        def scaleY(percentage):
            return mod.scale(percentage, config.screen_height)
        
        @staticmethod
        def scaleText(text, percentageOrPixels, style='mod_text', pixelTarget=False):
            try:
                import re
                
                if pixelTarget:
                    targetSize = mod.scalePx(percentageOrPixels)
                else:
                    targetSize = mod.scaleX(percentageOrPixels)
                text = re.sub('\{.*?\}', '', text)
                textLength = len(text)
                
                for currentLength in range(5, textLength+1):
                    if Text(text[:currentLength], None, False, False, style=style).size()[0] > targetSize: 
                        textLength = currentLength-1 
                        break
                
                if textLength < len(text):
                    return text[:textLength-1]+'...'
                else:
                    return text[:textLength]
            except:
                return text
        
        @staticmethod
        def max(val1, val2):
            return val1 if val1 > val2 else val2
        
        @staticmethod
        def min(val1, val2):
            return val1 if val1 < val2 else val2
        
        @staticmethod
        def touchDragged(drags, *args, **kwargs):
            try:
                mod.Settings.touchPosition = (drags[0].x, drags[0].y)
            except Exception as e:
                print('mod: Failed to save touchbutton position: {}'.format(e))
        
        
        class Confirm(NonPicklable):
            def __init__(self, prompt, yes=None, no=None, title=None, modal=True, promptSubstitution=True):
                self.prompt = prompt
                self.yes = yes
                self.no = no
                self.title = title
                self.modal = modal
                self.promptSubstitution = promptSubstitution
            
            def __call__(self):
                renpy.show_screen('mod_confirm', self.prompt, self.yes, self.no, self.title, self.modal, self.promptSubstitution)
                renpy.restart_interaction()
        
        class OpenConsole(NonPicklable):
            def __call__(self):
                _console.enter()

    class modReplay(NonPicklable):
        def __init__(self, label, finishAction=None, screenErrorVariable=None):
            self.label = label
            self.finishAction = finishAction
            self.screenErrorVariable = screenErrorVariable
            self._m1_main__error = None
            self._m1_main__currentScreen = None
        
        def _m1_main__replayErrorHandler(self, short, full, traceback_fn):
            self._m1_main__error = short
            return True
        
        def __call__(self):
            if not renpy.has_label(self.label):
                mod.Confirm('The selected label does not exist')()
            else:
                if self.screenErrorVariable:
                    self._m1_main__currentScreen = renpy.current_screen()
                
                
                replayScope = {}
                for k, v in globals().items():
                    if not k.startswith('_') and k != 'suppress_overlay':
                        replayScope[k] = v
                
                defaultErrorHandler = renpy.display.error.report_exception 
                renpy.display.error.report_exception = self._m1_main__replayErrorHandler 
                try:
                    renpy.call_replay(self.label, replayScope)
                except:
                    pass
                renpy.display.error.report_exception = defaultErrorHandler 
                
                if self._m1_main__error and self.screenErrorVariable and self._m1_main__currentScreen: 
                    if self.screenErrorVariable in self._m1_main__currentScreen.scope:
                        self._m1_main__currentScreen.scope['errorMessage'] = 'Replay failed with error:\n{}'.format(self._m1_main__error)
                elif self.finishAction:
                    self.finishAction()
                
                renpy.restart_interaction()


init 1999 python in _console:
    console = DebugConsole()

init 999 python:
    config.layers.append('mod') 
    mod.init()

    Loader.load_file('mod/mod_styles.rpy')
    Loader.load_file('mod/screens/main.rpy')
    Loader.load_file('mod/screens/search.rpy')
    Loader.load_file('mod/screens/vars.rpy')
    Loader.load_file('mod/screens/snapshots.rpy')
    Loader.load_file('mod/screens/labels.rpy')
    Loader.load_file('mod/screens/watchpanel.rpy')
    Loader.load_file('mod/screens/textbox.rpy')
    Loader.load_file('mod/screens/textrepl.rpy')
    Loader.load_file('mod/screens/choices.rpy')
    Loader.load_file('mod/screens/gamesaves.rpy')
    Loader.load_file('mod/screens/paths.rpy')
    Loader.load_file('mod/screens/options.rpy')
    Loader.load_file('mod/screens/utils.rpy')

    config.after_load_callbacks.append(mod.afterLoad)
    mod.LabelMon.onLabelCalled.append(mod.onLabelCalled)

    if mod.Settings.skipSplashscreen:
        config.label_overrides['splashscreen'] = 'mod_splashscreen'
