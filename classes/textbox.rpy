
init -1 python:
    class modTextBox(NonPicklable):
        def __init__(self):
            self._m1_textbox__originalSayArgCallback = None
            self._m1_textbox__originalShowScreen = None
            self.whoArgs = {}
            self.whatArgs = {}
            self._m1_textbox__imageTag = None
            self.previewCharacterVarName = None
            self.Settings = modTextBoxSettings()
            self.demoCharacter = Character('Name Character', image='Logo', color='#D4ADFC')
        
        @property
        def enabled(self):
            return bool(mod.Settings.textboxesEnabled or (self.Settings and self.Settings.tempValues != None))
        
        @enabled.setter
        def enabled(self, val):
            mod.Settings.textboxesEnabled = val
        
        def openCustomizer(self, charVarName=None, beforeOpenAction=None, afterCloseAction=None):
            self.Settings = modTextBoxSettings(charVarName)
            self.previewCharacter = charVarName
            if callable(beforeOpenAction): beforeOpenAction()
            renpy.call_in_new_context('mod_textboxCustomizer', charVarName=charVarName)
            if callable(afterCloseAction): afterCloseAction()
            
            
            raise renpy.game.RestartContext(None) 
        
        def closeCustomizer(self, save=False):
            if save:
                self.Settings.commitTemp(self.previewCharacterVarName)
            else:
                self.Settings.dismissTemp()
            renpy.jump('mod_textboxCustomizer_return')
        
        @property
        def previewCharacter(self):
            if self.previewCharacterVarName and hasattr(renpy.store, self.previewCharacterVarName):
                return getattr(renpy.store, self.previewCharacterVarName)
            
            return self.demoCharacter
        
        @previewCharacter.setter
        def previewCharacter(self, val):
            if val and hasattr(renpy.store, val) and isinstance(getattr(renpy.store, val), ADVCharacter):
                self.previewCharacterVarName = val
            else:
                self.previewCharacterVarName = None
        
        @property
        def textHeight(self):
            return mod.scalePxInt(self.Settings.whatHeight)
        
        @property
        def sideImage(self):
            if not self._m1_textbox__imageTag: return None
            
            if self._m1_textbox__imageTag == 'Logo':
                img = 'mod/images/logo.png'
            else:
                img = renpy.get_registered_image('{} {}'.format(config.side_image_prefix_tag, self._m1_textbox__imageTag))
            
            if img:
                try:
                    return mod_ScaleImage(img, mod.TextBox.textHeight, mod.TextBox.textHeight)
                except:
                    print('mod: Failed to get side image "{}"'.format(self._m1_textbox__imageTag))
        
        @property
        def whatXPadding(self):
            return mod.scalePxInt(self.Settings.whatXPadding or 0)
        
        @property
        def whoXPadding(self):
            return mod.scalePxInt(self.Settings.whoXPadding or 0)
        
        @property
        def whoXAlign(self):
            return self.Settings.whoXAlign or 0.0
        
        @property
        def whoBackground(self):
            if self.Settings.whoBackgroundEnabled:
                if self.Settings.whoBackgroundCharacterColor and ('color' in self.whoArgs or self.Settings.whoColor):
                    if 'color' in self.whoArgs:
                        color = self._m1_textbox__appendColorAlpha(self.whoArgs['color'], self.Settings.whoBackground)
                    else:
                        color = self._m1_textbox__appendColorAlpha(self.Settings.whoColor, self.Settings.whoBackground)
                else:
                    color = self.Settings.whoBackground
                
                if self.Settings.whoBackgroundGradient:
                    return AlphaMask(Solid(color), Frame('mod/images/textboxGradientCentered.png'))
                else:
                    return Solid(color)
        
        @property
        def whoFont(self):
            if self.Settings.whoFont and self.Settings.whoFont in modTextBoxSettings.fontOptions and renpy.loadable(modTextBoxSettings.fontOptions[self.Settings.whoFont]):
                return modTextBoxSettings.fontOptions[self.Settings.whoFont]
            else:
                return list(modTextBoxSettings.fontOptions.values())[0]
        
        @property
        def whatBackground(self):
            if self.Settings.whatBackgroundEnabled:
                if self.Settings.whatBackgroundCharacterColor and ('color' in self.whoArgs or self.Settings.whoColor):
                    if 'color' in self.whoArgs:
                        color = self._m1_textbox__appendColorAlpha(self.whoArgs['color'], self.Settings.whatBackground)
                    else:
                        color = self._m1_textbox__appendColorAlpha(self.Settings.whoColor, self.Settings.whatBackground)
                else:
                    color = self.Settings.whatBackground
                
                if self.Settings.whatBackgroundGradient:
                    return AlphaMask(Solid(color), Frame('mod/images/textboxGradient.png'))
                else:
                    return Solid(color)
        
        @property
        def whatFont(self):
            if self.Settings.whatFont and self.Settings.whatFont in modTextBoxSettings.fontOptions and renpy.loadable(modTextBoxSettings.fontOptions[self.Settings.whatFont]):
                return modTextBoxSettings.fontOptions[self.Settings.whatFont]
            else:
                return list(modTextBoxSettings.fontOptions.values())[0]
        
        def _m1_textbox__appendColorAlpha(self, baseColor, alphaColor):
            """ Transfer the alpha channel from `alphaColor` to `baseColor` """
            if len(alphaColor) == 5:
                alphaValue = alphaColor[-1:]*2
            elif len(alphaColor) == 9:
                alphaValue = alphaColor[-2:]
            else:
                return baseColor 
            
            if len(baseColor) == 4 or len(baseColor) == 5:
                return '#{}{}{}{}'.format(baseColor[1]*2, baseColor[2]*2, baseColor[3]*2, alphaValue)
            elif len(baseColor) == 7 or len(baseColor) == 9:
                return '#{}{}{}{}'.format(baseColor[1:3], baseColor[3:5], baseColor[5:7], alphaValue)
            else:
                return baseColor
        
        def _m1_textbox__createWhoArgs(self, args):
            args = self._m1_textbox__stripUnwantedStyleArgs(args)
            
            
            if self.Settings.customSayScreen or self.Settings.whoFont != None: args['font'] = self.whoFont
            if self.Settings.whoColor != None: args['color'] = self.Settings.whoColor
            if self.Settings.whoOutlinesEnabled:
                args['outlines'] = [(absolute(self.Settings.whoOutlinesWidth or 0), self.Settings.whoOutlinesColor or '#000', absolute(1), absolute(1)),(absolute(self.Settings.whoOutlinesWidth or 0), self.Settings.whoOutlinesColor or '#000', absolute(-1), absolute(-1))]
            else:
                args['outlines'] = []
            if self.Settings.whoBold != None: args['bold'] = self.Settings.whoBold
            if self.Settings.whoItalic != None: args['italic'] = self.Settings.whoItalic
            if self.Settings.whoXAlign != None: args['xalign'] = self.Settings.whoXAlign
            args['size'] = mod.scalePxInt(self.Settings.whoSize or modTextBoxSettings.defaultValues['whoSize'])
            
            if not self.Settings.customSayScreen:
                args = self._m1_textbox__stripDisallowedSayArgs(args)
            
            return args
        
        def _m1_textbox__createWhatArgs(self, args):
            args = self._m1_textbox__stripUnwantedStyleArgs(args)
            
            
            args['style'] = 'modSay_text'
            if self.Settings.customSayScreen or self.Settings.whatFont != None: args['font'] = self.whatFont
            if self.Settings.whatColorFromCharacter and 'color' in self.whoArgs:
                args['color'] = self._m1_textbox__appendColorAlpha(self.whoArgs['color'], self.Settings.whatColor or '#fff')
            elif self.Settings.whatColor != None:
                args['color'] = self.Settings.whatColor
            if self.Settings.whatOutlinesEnabled:
                args['outlines'] = [(absolute(self.Settings.whatOutlinesWidth or 0), self.Settings.whatOutlinesColor or '#000', absolute(1), absolute(1)),(absolute(self.Settings.whatOutlinesWidth or 0), self.Settings.whatOutlinesColor or '#000', absolute(-1), absolute(-1))]
            else:
                args['outlines'] = []
            if self.Settings.whatBold != None: args['bold'] = self.Settings.whatBold
            if self.Settings.whatItalic != None: args['italic'] = self.Settings.whatItalic
            args['size'] = mod.scalePxInt(self.Settings.whatSize or modTextBoxSettings.defaultValues['whatSize'])
            args['textalign'] = self.Settings.whatAlign
            args['xalign'] = self.Settings.whatAlign
            
            
            prefixedArgs = {}
            for key,val in args.items():
                prefixedArgs['what_{}'.format(key)] = val
            
            if not self.Settings.customSayScreen:
                prefixedArgs = self._m1_textbox__stripDisallowedSayArgs(prefixedArgs)
            
            return prefixedArgs
        
        def _m1_textbox__stripUnwantedStyleArgs(self, args):
            """ Remove unwanted styling arguments """
            allowedArgs = ['color','italic','bold','outlines','slow_abortable']
            newArgs = {}
            
            for arg in args:
                if not self.Settings.customSayScreen or arg in allowedArgs:
                    newArgs[arg] = args[arg]
            
            return newArgs
        
        def _m1_textbox__stripDisallowedSayArgs(self, args):
            """ Strip argument that are not allowed when using the default say screen """
            disallowedArgs = ['xalign','textalign','style','what_xalign','what_textalign','what_style']
            newArgs = {}
            
            for arg in args:
                if not arg in disallowedArgs:
                    newArgs[arg] = args[arg]
            
            return newArgs
        
        def _m1_textbox__sayReplace(self, who, *args, **kwargs):
            if self._m1_textbox__originalSayArgCallback:
                args, kwargs = self._m1_textbox__originalSayArgCallback(who, *args, **kwargs)
            
            if self.enabled:
                if not renpy.get_screen('mod_textboxCustomizer'): 
                    self.Settings = modTextBoxSettings(who)
                if self.Settings.customSayScreen:
                    kwargs['screen'] = 'mod_say' 
                self._m1_textbox__imageTag = who.image_tag if hasattr(who, 'image_tag') else None
                self.whoArgs = self._m1_textbox__createWhoArgs(who.who_args if hasattr(who, 'who_args') else {})
                self.whatArgs = self._m1_textbox__createWhatArgs(who.what_args if hasattr(who, 'what_args') else {})
                kwargs.update(self.whoArgs)
                kwargs.update(self.whatArgs)
            
            return args, kwargs
        
        def _m1_textbox__captureSayScreen(self, screenName, *args, **kwargs):
            """
            Ren'Py will call the original say screen with kwargs={'who': None, 'what': ''} to show the screen's transition, before opening the actual (filled) say screen.
            This will prevent Ren'Py from showing the `config.window_show_transition` and `config.window_hide_transition`.
            """
            if self.enabled and screenName == 'say' and 'who' in kwargs and not kwargs['who'] and 'what' in kwargs and not kwargs['what']: 
                pass
            else:
                self._m1_textbox__originalShowScreen(screenName, *args, **kwargs)
        
        def attach(self):
            if config.say_arguments_callback != self._m1_textbox__sayReplace: 
                self._m1_textbox__originalSayArgCallback = config.say_arguments_callback
                config.say_arguments_callback = self._m1_textbox__sayReplace
            
            if renpy.display.screen.show_screen != self._m1_textbox__captureSayScreen:
                self._m1_textbox__originalShowScreen = renpy.display.screen.show_screen
                renpy.display.screen.show_screen = self._m1_textbox__captureSayScreen

    class modTextBoxSettings(NonPicklable):
        defaultValues = {
            
            'customSayScreen': True, 
            
            'whoShown': True,
            'whoColor': None,
            'whoOutlinesEnabled': True,
            'whoOutlinesWidth': 2,
            'whoOutlinesColor': '#000',
            'whoBold': None,
            'whoItalic': None,
            'whoSize': 32,
            'whoXAlign': 0.0,
            'whoXPadding': 10,
            'whoBackgroundEnabled': False,
            'whoBackground': '#1D267D99',
            'whoBackgroundGradient': False,
            'whoBackgroundCharacterColor': False,
            'whoFont': None,
            
            'sideImageShown': True,
            'sideImagePos': 'left',
            
            'whatColor': None,
            'whatColorFromCharacter': False,
            'whatOutlinesEnabled': True,
            'whatOutlinesWidth': 2,
            'whatOutlinesColor': '#000',
            'whatBold': None,
            'whatItalic': None,
            'whatSize': 32,
            'whatAlign': 0.0,
            'whatXPadding': 10,
            'whatHeight': 150,
            'whatBackgroundEnabled': True,
            'whatBackground': '#5C469C99',
            'whatBackgroundGradient': True,
            'whatBackgroundCharacterColor': False,
            'whatFont': None,
        }
        fontOptions = modOrderedDict([
            ('DejaVu Sans', 'DejaVuSans.ttf'),
            ('Roboto', 'mod/Roboto-Regular.ttf'),
            ('Roboto Mono', 'mod/RobotoMono.ttf'),
            ('Dancing Script', 'mod/DancingScript.ttf'),
            ('Caveat', 'mod/Caveat.ttf'),
            ('Comfortaa', 'mod/Comfortaa.ttf'),
        ])
        
        _m1_textbox__tempValues = None
        _m1_textbox__values = None
        _m1_textbox__valuesChar = None 
        
        def __init__(self, char=None):
            modTextBoxSettings._m1_textbox__tempValues = None
            
            if modTextBoxSettings._m1_textbox__valuesChar != char: 
                modTextBoxSettings._m1_textbox__values = self._m1_textbox__getSettingsForChar(char)
                modTextBoxSettings._m1_textbox__valuesChar = char 
        
        @property
        def tempValues(self):
            return modTextBoxSettings._m1_textbox__tempValues
        
        @property
        def values(self):
            return modTextBoxSettings._m1_textbox__values
        
        def _m1_textbox__getSettingsForChar(self, char):
            if mod.Loader.textboxCustomizations: 
                if isinstance(char, basestring) and char in mod.Loader.textboxCustomizations: 
                    return mod.Loader.textboxCustomizations[char]
                elif isinstance(char, ADVCharacter): 
                    for charVarName in mod.Loader.textboxCustomizations.keys():
                        if hasattr(renpy.store, charVarName) and getattr(renpy.store, charVarName) == char:
                            return mod.Loader.textboxCustomizations[charVarName]
                
                
                if 'None' in mod.Loader.textboxCustomizations:
                    return mod.Loader.textboxCustomizations['None']
        
        def enableTemp(self, charVarName):
            modTextBoxSettings._m1_textbox__tempValues = (self._m1_textbox__getSettingsForChar(charVarName) or {}).copy()
        
        def commitTemp(self, charVarName):
            if self.tempValues:
                mod.Loader.setTextboxCustomization(self.tempValues, charVarName)
                modTextBoxSettings._m1_textbox__tempValues = None
        
        def dismissTemp(self):
            modTextBoxSettings._m1_textbox__tempValues = None
            renpy.restart_interaction()
        
        def __getattr__(self, attr):
            if attr in modTextBoxSettings.defaultValues:
                return self.get(attr)
        
        def __setattr__(self, attr, value):
            if attr in modTextBoxSettings.defaultValues:
                self.set(attr, value)
        
        def get(self, name):
            if self.tempValues != None:
                if name in self.tempValues:
                    return self.tempValues[name]
            elif self.values and name in self.values:
                return self.values[name]
            
            
            if name in modTextBoxSettings.defaultValues:
                return modTextBoxSettings.defaultValues[name]
        
        def set(self, name, value):
            if self.tempValues != None:
                self.tempValues[name] = value
            
            renpy.restart_interaction()

    class modTextBoxSettingCallback(NonPicklable):
        def __init__(self, settingName):
            self.settingName = settingName
        
        def __call__(self, value):
            setattr(mod.TextBox.Settings, self.settingName, value)

init 999 python:

    mod.TextBox.attach()
