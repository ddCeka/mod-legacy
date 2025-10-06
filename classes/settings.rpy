
init -1 python:

    class modSettingsClass(NonPicklable):
        defaultValues = {
            'lastLoadedFile': None,
            'labelsView': 'thumbnails',
            'searchRecursive': False,
            'searchPersistent': True,
            'searchObjects': True,
            'showUnsupportedVariables': False,
            'useWildcardSearch': False,
            'showWatchPanel': False,
            'collapsedWatchPanel': False,
            'watchpanelToggleKey': '',
            'watchpanelHideToggleButton': False,
            'watchPanelPos': 'l',
            'showChoicesNotification': True,
            'showPathsNotification': True,
            'stopSkippingOnPathDetection': False,
            'showReplayNotification': True,
            'currentScreen': 'search',
            'searchType': 'variable names',
            'askSaveName': False,
            'quickResumeSaveHotKey': False,
            'quickSaveHotKey': False,
            'quickLoadHotKey': False,
            'consoleHotKey': False,
            'skipSplashscreen': False,
            'touchEnabled': False,
            'touchPosition': None,
            'textboxesEnabled': False,
        }
        
        _m1_settings__saveDir = None
        _m1_settings__globalSettings = {}
        _m1_settings__id = None
        
        def __init__(self):
            import __main__
            
            modSettingsClass._m1_settings__saveDir = __main__.path_to_saves(renpy.config.gamedir, '.mod')
            if self.saveDir and not renpy.os.path.isdir(self.saveDir): 
                try:
                    renpy.os.mkdir(self.saveDir)
                except Exception as e:
                    print('mod: Failed to create dir "{}". {}'.format(self.saveDir, e))
                    modSettingsClass._m1_settings__saveDir = None
            
            self._m1_settings__loadGlobalSettings()
        
        @property
        def saveDir(self):
            return modSettingsClass._m1_settings__saveDir
        
        @property
        def id(self):
            return modSettingsClass._m1_settings__id
        
        def saveId(self, val):
            modSettingsClass._m1_settings__id = val
            self._m1_settings__saveGlobalSettings()
        
        def __getattr__(self, attr):
            if attr in modSettingsClass.defaultValues:
                return self.get(attr)
            else:
                print('mod: Something requested an unknown setting "{}"'.format(attr))
        
        def __setattr__(self, attr, value):
            if attr in modSettingsClass.defaultValues:
                self.set(attr, value)
        
        def get(self, name, globalSetting=None):
            defaultValue = None
            if name in modSettingsClass.defaultValues: defaultValue = modSettingsClass.defaultValues[name]
            
            if globalSetting: 
                if name in modSettingsClass._m1_settings__globalSettings:
                    return modSettingsClass._m1_settings__globalSettings[name]
                else:
                    return defaultValue
            
            elif globalSetting == False: 
                if persistent.modSettings != None and name in persistent.modSettings:
                    return persistent.modSettings[name]
            
            else: 
                if persistent.modSettings != None and name in persistent.modSettings:
                    return persistent.modSettings[name]
                elif name in modSettingsClass._m1_settings__globalSettings:
                    return modSettingsClass._m1_settings__globalSettings[name]
                else:
                    return defaultValue
        
        def set(self, name, value, globalSetting=None):
            if globalSetting:
                if value == None and name in modSettingsClass._m1_settings__globalSettings: 
                    del modSettingsClass._m1_settings__globalSettings[name]
                else:
                    modSettingsClass._m1_settings__globalSettings[name] = value
                
                self._m1_settings__saveGlobalSettings() 
            else:
                if persistent.modSettings == None:
                    persistent.modSettings = {name: value}
                elif value == None and name in persistent.modSettings: 
                    del persistent.modSettings[name]
                else:
                    persistent.modSettings[name] = value
            
            renpy.restart_interaction()
        
        def _m1_settings__loadGlobalSettings(self):
            if not self.saveDir: return 
            
            import zipfile, json
            fileName = renpy.os.path.join(self.saveDir, 'settings')
            if renpy.os.path.exists(fileName):
                try:
                    with zipfile.ZipFile(fileName, 'r') as zf:
                        jsonStr = zf.read('json')
                        modSettingsClass._m1_settings__id = zf.read('id')
                        modVersion = zf.read('modVersion')
                    
                    
                    modSettingsClass._m1_settings__globalSettings = json.loads(jsonStr)
                except Exception as e:
                    print('mod: Failed to read global settings from {}. {}'.format(fileName, e))
        
        def _m1_settings__saveGlobalSettings(self):
            if not self.saveDir: return 
            
            import zipfile, shutil, json
            fileName = renpy.os.path.join(self.saveDir, 'settings')
            fileNameNew = fileName + '.new'
            try:
                with zipfile.ZipFile(fileNameNew, 'w', zipfile.ZIP_DEFLATED) as zf:
                    zf.writestr('json', json.dumps(modSettingsClass._m1_settings__globalSettings))
                    if self.id: zf.writestr('id', self.id)
                    zf.writestr('modVersion', mod.version)
                
                shutil.move(fileNameNew, fileName)
            except Exception as e:
                print('mod: Failed to save global settings to {}. {}'.format(fileName, e))
                raise e

    class SetmodSetting(renpy.ui.Action):
        def __init__(self, name, value, globalSetting=False):
            self.name = name
            self.value = value
            self.globalSetting = globalSetting
        
        def __call__(self):
            mod.Settings.set(self.name, self.value, self.globalSetting)
        
        def get_selected(self):
            return mod.Settings.get(self.name, self.globalSetting) == self.value
