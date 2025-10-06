
init -1 python:

    class modLoader(NonPicklable):
        def __init__(self):
            self.rememberedVars = modOrderedDict()
            self.rememberedLabels = modOrderedDict()
            self.watchedVars = modOrderedDict()
            self.frozenVars = []
            self.monitoredVars = []
            self.textboxCustomizations = modOrderedDict()
            self.loadedFile = ''
            self.unsavedChanges = False
            
            self._m1_loader__saveDir = None 
            self.gameDir = renpy.os.path.abspath(renpy.os.path.join(config.basedir, "game"))
        
        @property
        def saveDir(self):
            if self._m1_loader__saveDir == None:
                self._m1_loader__saveDir = renpy.os.path.abspath(renpy.os.path.join(mod.Settings.saveDir, config.save_directory)) 
                
                
                try:
                    renpy.os.makedirs(self.saveDir)
                except Exception:
                    pass
            
            return self._m1_loader__saveDir
        
        def autoLoad(self):
            """ Auto load the `lastLoadedFile` if nothing is loaded """
            if not self.loadedFile and mod.Settings.lastLoadedFile != None and len(self.rememberedVars) == 0 and len(self.rememberedLabels) == 0 and len(self.watchedVars) == 0:
                self.load(mod.Settings.lastLoadedFile)
        
        def rememberVar(self, varName, displayName=None):
            """ Add `varName` to remembered list """
            if callable(displayName): displayName = displayName()
            
            if varName in self.rememberedVars:
                self.rememberedVars[varName] = {'name': displayName or self.rememberedVars[varName]['name']}
            else:
                self.rememberedVars[varName] = {'name': displayName or varName}
            self.unsavedChanges = True
        
        def forgetVar(self, varName):
            """ Remove `varName` from remembered list """
            if self.hasVar(varName):
                del self.rememberedVars[varName]
                if varName in self.frozenVars: self.frozenVars.remove(varName)
                if varName in self.monitoredVars: self.monitoredVars.remove(varName)
                self.unsavedChanges = True
        
        def changeVarPos(self, sourceVarName, targetVarName):
            if self.hasVar(sourceVarName) and self.hasVar(targetVarName):
                self.rememberedVars.changePos(sourceVarName, targetVarName)
                self.unsavedChanges = True
        
        def sortVars(self, reverse=False):
            self.rememberedVars.sort(reverse, sortByAttr='name')
            self.unsavedChanges = True
        
        def rememberLabel(self, labelName, displayName):
            """ Add `labelName` to remembered labels list """
            if callable(displayName): displayName = displayName()
            
            self.rememberedLabels[labelName] = {'name': displayName}
            self.unsavedChanges = True
        
        def forgetLabel(self, labelName):
            """ Revove `labelName` from remembered labels list """
            if self.hasLabel(labelName):
                del self.rememberedLabels[labelName]
                self.unsavedChanges = True
        
        def changeLabelPos(self, sourceLabelName, targetLabelName):
            if self.hasLabel(sourceLabelName) and self.hasLabel(targetLabelName):
                self.rememberedLabels.changePos(sourceLabelName, targetLabelName)
                self.unsavedChanges = True
        
        def sortLabels(self, reverse=False):
            self.rememberedLabels.sort(reverse, sortByAttr='name')
            self.unsavedChanges = True
        
        def watchVar(self, varName, displayName):
            """Add `varName` to watchlist """
            if callable(displayName): displayName = displayName()
            
            self.watchedVars[varName] = {'name': displayName}
            self.unsavedChanges = True
            mod.Settings.showWatchPanel = True 
        
        def unwatchVar(self, varName):
            """ Remove `varName` from watch list """
            if self.isWatchingVar(varName):
                del self.watchedVars[varName]
                self.unsavedChanges = True
        
        def freezeVar(self, varName):
            if not varName in self.frozenVars:
                self.frozenVars.append(varName)
                self.rememberVar(varName, None)
        
        def unfreezeVar(self, varName):
            if varName in self.frozenVars:
                self.frozenVars.remove(varName)
        
        def freezableVar(self, varName):
            if '.' in varName:
                return False
            return True
        
        def monitorVar(self, varName):
            if not varName in self.monitoredVars:
                self.monitoredVars.append(varName)
                self.rememberVar(varName, None)
        
        def unmonitorVar(self, varName):
            if varName in self.monitoredVars:
                self.monitoredVars.remove(varName)
        
        def monitorableVar(self, varName):
            if '.' in varName:
                return False
            return True
        
        def setTextboxCustomization(self, settings, charVarName=None):
            if settings:
                self.textboxCustomizations[str(charVarName)] = settings
            elif str(charVarName) in self.textboxCustomizations:
                del self.textboxCustomizations[charVarName]
            self.unsavedChanges = True
        
        def changeVarWatchPos(self, sourceVarName, targetVarName):
            if self.isWatchingVar(sourceVarName) and self.isWatchingVar(targetVarName):
                self.watchedVars.changePos(sourceVarName, targetVarName)
                self.unsavedChanges = True
        
        def sortWatchedVars(self, reverse=False):
            self.watchedVars.sort(reverse, sortByAttr='name')
            self.unsavedChanges = True
        
        def clear(self):
            """ Start a new file """
            if self.unsavedChanges:
                mod.Confirm('Unsaved changes will be lost, do you want to continue?', self.clearRemembered)()
            else:
                self.clearRemembered()
        
        def clearRemembered(self):
            self.clearVars()
            self.clearLabels()
            self.clearWatchedVars()
            mod.TextRepl.clearReplacements()
            self.clearTextboxCustomizations()
            self.loadedFile = ''
            mod.Settings.lastLoadedFile = None
            self.unsavedChanges = False
        
        def clearVars(self):
            self.rememberedVars = modOrderedDict()
            self.frozenVars = []
            self.monitoredVars = []
            self.unsavedChanges = True
        
        def clearLabels(self):
            self.rememberedLabels = modOrderedDict()
            self.unsavedChanges = True
        
        def clearWatchedVars(self):
            self.watchedVars = modOrderedDict()
            self.unsavedChanges = True
        
        def clearTextboxCustomizations(self):
            self.textboxCustomizations = modOrderedDict()
            self.unsavedChages = True
        
        def hasVar(self, varName):
            return (varName in self.rememberedVars)
        
        def hasLabel(self, labelName):
            return (labelName in self.rememberedLabels)
        
        def isWatchingVar(self, varName):
            return (varName in self.watchedVars)
        
        def isFrozenVar(self, varName):
            return (varName in self.frozenVars)
        
        def isMonitoredVar(self, varName):
            return (varName in self.monitoredVars)
        
        def fileExists(self, filename):
            return renpy.exists(renpy.os.path.join(self.gameDir, filename)) or renpy.exists(renpy.os.path.join(self.saveDir, filename))
        
        def listFiles(self):
            import re
            from glob import glob
            from collections import OrderedDict
            
            files = {}
            
            
            gameDirFiles = glob(renpy.os.path.join(re.sub(r'(\[|\])', r'[\1]', self.gameDir), '*.mod')) 
            for i,filename in enumerate(gameDirFiles):
                files[filename[len(self.gameDir)+1:]] = {'filename': filename, 'mtime': renpy.os.path.getmtime(filename)}
            
            
            saveDirFiles = glob(renpy.os.path.join(re.sub(r'(\[|\])', r'[\1]', self.saveDir), '*.mod')) 
            for i,filename in enumerate(saveDirFiles):
                mtime = renpy.os.path.getmtime(filename)
                name = filename[len(self.saveDir)+1:]
                if not hasattr(files, name) or files[name].mtime < mtime:
                    files[name] = {'filename': filename, 'mtime': mtime}
            
            
            files = OrderedDict(sorted(files.items()))
            
            return files
        
        def stripSpecialChars(self, str):
            import re
            return re.sub('[^A-Za-z0-9 _-]', '_', str)
        
        class Save(NonPicklable):
            def __init__(self, filename=None, finishAction=None, screenErrorVariable=None):
                self.filename = filename
                self.finishAction = finishAction
                self.screenErrorVariable = screenErrorVariable
            
            def __call__(self):
                cs = renpy.current_screen()
                
                def onSuccess():
                    if self.finishAction:
                        self.finishAction()
                
                def onFailure():
                    if self.screenErrorVariable and cs and self.screenErrorVariable in cs.scope:
                        cs.scope[self.screenErrorVariable] = 'Failed to save file'
                        renpy.restart_interaction()
                
                mod.Loader.save(self.filename if not callable(self.filename) else self.filename(), onSuccess, onFailure)
        
        def save(self, name=None, success=None, failure=None, overwrite=False):
            if name == None: 
                if len(self.rememberedVars) == 0 and len(self.rememberedLabels) == 0 and len(self.watchedVars) == 0 and len(mod.TextRepl.replacements) == 0 and len(self.textboxCustomizations) == 0:
                    renpy.notify("There's nothing to save")
                else:
                    renpy.show_screen('mod_save_file')
                    renpy.restart_interaction()
            else:
                filename = self.stripSpecialChars(name)+'.mod'
                if self.fileExists(filename) and not overwrite:
                    return mod.Confirm('Do you want to overwrite the existing file?', Function(self.save, name, success, failure, True))()
                else:
                    
                    for key in self.rememberedVars:
                        self.rememberedVars[key]['frozen'] = self.isFrozenVar(key)
                        self.rememberedVars[key]['monitored'] = self.isMonitoredVar(key)
                    
                    
                    if self._m1_loader__saveFile(filename, {'vars': self.rememberedVars, 'labels': self.rememberedLabels, 'watched': self.watchedVars, 'replacements': [mod.TextRepl.replacements[k].__dict__ for k in mod.TextRepl.replacements], 'textboxCustomizations': self.textboxCustomizations}):
                        renpy.notify('Saved to game directory')
                        self.unsavedChanges = False
                        self.loadedFile = filename
                        mod.Settings.lastLoadedFile = filename
                        
                        if success:
                            success()
                        else:
                            return True
                    else:
                        if failure:
                            failure()
                        else:
                            return False
        
        def _m1_loader__saveFile(self, filename, data):
            import json
            
            gameDirPath = renpy.os.path.join(self.gameDir, filename)
            saveDirPath = renpy.os.path.join(self.saveDir, filename)
            
            
            try:
                jsonData = json.dumps(data)
            except Exception as e:
                print('mod: Converting savedata failed with error: {}'.format(e))
                return False
            
            
            try:
                f = renpy.os.open(gameDirPath, renpy.os.O_CREAT | renpy.os.O_WRONLY | renpy.os.O_TRUNC)
                renpy.os.write(f, jsonData.encode(encoding='UTF-8'));
                renpy.os.close(f)
            except Exception as e:
                print('mod: Failed to save file "{}" with error: {}'.format(gameDirPath, e))
                return False
            
            
            try:
                f = renpy.os.open(saveDirPath, renpy.os.O_CREAT | renpy.os.O_WRONLY | renpy.os.O_TRUNC)
                renpy.os.write(f, jsonData.encode(encoding='UTF-8'));
                renpy.os.close(f)
            except Exception as e:
                print('mod: Failed to save file "{}" with error: {}'.format(saveDirPath, e))
            
            return True
        
        class Load(NonPicklable):
            def __init__(self, filename=None, finishAction=None, screenErrorVariable=None):
                self.filename = filename
                self.finishAction = finishAction
                self.screenErrorVariable = screenErrorVariable
            
            def __call__(self):
                if mod.Loader.load(self.filename):
                    if self.finishAction:
                        self.finishAction()
                elif self.screenErrorVariable: 
                    cs = renpy.current_screen()
                    if cs and self.screenErrorVariable in cs.scope:
                        cs.scope[self.screenErrorVariable] = 'Failed to load file'
                        renpy.restart_interaction()
        
        def load(self, filename=None):
            if not filename:
                if self.unsavedChanges:
                    mod.Confirm('Unsaved changes will be lost, do you want to continue?', Show('mod_load_file'))()
                else:
                    renpy.show_screen('mod_load_file')
                    renpy.restart_interaction()
            else:
                data = self._m1_loader__loadFile(filename)
                if data:
                    if 'vars' in data:
                        self.rememberedVars = data['vars']
                        
                        self.frozenVars = []
                        self.monitoredVars = []
                        for varName in self.rememberedVars:
                            if 'frozen' in self.rememberedVars[varName] and self.rememberedVars[varName]['frozen']:
                                self.frozenVars.append(varName)
                            if 'monitored' in self.rememberedVars[varName] and self.rememberedVars[varName]['monitored']:
                                self.monitoredVars.append(varName)
                    else:
                        self.rememberedVars = {}
                    if 'labels' in data:
                        self.rememberedLabels = data['labels']
                    else:
                        self.rememberedLabels = {}
                    if 'watched' in data:
                        self.watchedVars = data['watched']
                    else:
                        self.watchedVars = {}
                    if 'replacements' in data:
                        for replacement in data['replacements']:
                            mod.TextRepl.addReplacement(modTextReplacement(**replacement))
                    else:
                        mod.TextRepl.clearReplacements()
                    if 'textboxCustomizations' in data:
                        self.textboxCustomizations = data['textboxCustomizations']
                    self.unsavedChanges = False
                    self.loadedFile = filename
                    mod.Settings.lastLoadedFile = filename
                    return True
                
                return False
        
        def _m1_loader__loadFile(self, filename):
            import json
            
            gameDirPath = renpy.os.path.join(self.gameDir, filename)
            saveDirPath = renpy.os.path.join(self.saveDir, filename)
            
            
            gameDirMtime = renpy.os.path.getmtime(gameDirPath) if renpy.os.path.isfile(gameDirPath) else 0
            saveDirMtime = renpy.os.path.getmtime(saveDirPath) if renpy.os.path.isfile(saveDirPath) else 0
            
            
            selectedFile = None
            if gameDirMtime >= saveDirMtime and gameDirMtime > 0:  
                selectedFile = gameDirPath
            elif saveDirMtime > 0: 
                selectedFile = saveDirPath
            
            
            if selectedFile:
                try:
                    f = renpy.os.open(selectedFile, renpy.os.O_RDONLY) 
                    jsonData = json.loads(renpy.os.read(f, renpy.os.path.getsize(selectedFile)), object_pairs_hook=modOrderedDict)
                    renpy.os.close(f)
                    return jsonData
                except Exception as e:
                    print('mod: Loading file "{}" failed with error: {}'.format(filename, e))
                    return None
        
        class Delete(NonPicklable):
            def __init__(self, filename):
                self.filename = filename
            
            def __call__(self):
                import json, os
                
                gameDirPath = renpy.os.path.join(mod.Loader.gameDir, self.filename)
                saveDirPath = renpy.os.path.join(mod.Loader.saveDir, self.filename)
                
                try:
                    if renpy.os.path.isfile(gameDirPath):
                        renpy.os.remove(gameDirPath)
                except Exception as e:
                    print('mod: Failed to delete file "{}" with error: {}'.format(gameDirPath, e))
                
                try:
                    if renpy.os.path.isfile(saveDirPath):
                        renpy.os.remove(saveDirPath)
                except Exception as e:
                    print('mod: Failed to delete file "{}" with error: {}'.format(saveDirPath, e))
