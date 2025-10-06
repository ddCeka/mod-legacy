
init -1 python:

    class modVar(NonPicklable):
        _m1_vars__expandedVarNames = []
        
        def __init__(self, varName, storeDict=None):
            self._m1_vars__varName = varName
            self._m1_vars__storeDict = storeDict
        
        @property
        def name(self):
            return self._m1_vars__varName
        
        @property
        def storeDict(self):
            return self._m1_vars__storeDict or renpy.store.__dict__
        
        @property
        def varType(self):
            if not hasattr(self, '__varType'):
                self._m1_vars__varType = modVar.getValType(self.value)
            return self._m1_vars__varType
        
        @property
        def isExpandable(self):
            if not hasattr(self, '__isExpandable'):
                self._m1_vars__isExpandable = (self.varType in ['list', 'dict'] or self.varType.startswith('<class'))
            return self._m1_vars__isExpandable
        
        @property
        def expanded(self):
            return self.name in modVar._m1_vars__expandedVarNames
        
        @expanded.setter
        def expanded(self, val):
            if val == False and self.expanded == True:
                modVar._m1_vars__expandedVarNames.remove(self.name)
            elif val == True and self.expanded == False:
                modVar._m1_vars__expandedVarNames.append(self.name)
        
        @property
        def isSupported(self):
            if not hasattr(self, '__isSupported'):
                self._m1_vars__isSupported = modVar.isSupportedVarType(self.varType)
            return self._m1_vars__isSupported
        
        @property
        def isEditable(self):
            return not bool(self._m1_vars__storeDict)
        
        @property
        def namePath(self):
            """
            Split list, dict and object names.
            `var1.var2[3].var4["var 5"]` will become a list ['var1','.var2','[3]','.var4','["var 5"]']
            """
            parentName = renpy.re.findall(r"^(\w+)[\.\]]?", self.name)
            if len(parentName) != 1:
                return [self.name]
            
            children = renpy.re.findall(r"(\.\w+|\[\d+\]|\[[\"\'][\w\ ]+[\"\']\])", self.name)
            return parentName + children
        
        @property
        def value(self):
            try:
                
                currentValue = None
                for index,currentPath in enumerate(self.namePath):
                    if index == 0:
                        if currentPath in self.storeDict:
                            currentValue = self.storeDict[currentPath]
                        else:
                            return None 
                    else: 
                        if currentPath.startswith('.'): 
                            if hasattr(currentValue, currentPath[1:]):
                                currentValue = getattr(currentValue, currentPath[1:])
                            else:
                                return None
                        elif renpy.re.match(r"^\[[\"\'].+[\"\']\]$", currentPath): 
                            if currentPath[2:-2] in currentValue:
                                currentValue = currentValue[currentPath[2:-2]]
                            else:
                                return None
                        elif renpy.re.match(r"^\[\d+\]$", currentPath): 
                            currentIndex = int(currentPath[1:-1])
                            if isinstance(currentValue, list) and len(currentValue) > currentIndex:
                                currentValue = currentValue[currentIndex]
                            else:
                                return None
                
                return currentValue
            except:
                pass
        
        def setValue(self, newValue, overruleVarType=None, operator='=', varChildKey=None):
            if not self.isEditable: return False 
            if callable(newValue): newValue = newValue()
            if callable(overruleVarType): overruleVarType = overruleVarType()
            if callable(operator): operator = operator()
            if callable(varChildKey): varChildKey = varChildKey()
            
            settableVar = self if not varChildKey else self.getChild(varChildKey)
            
            varType = overruleVarType or settableVar.varType
            isFrozen = mod.Loader.isFrozenVar(self._m1_vars__varName)
            try:
                settableValue = None
                if varType == 'string':
                    settableValue = '"""'+newValue+'"""'
                elif varType == 'boolean':
                    settableValue = str(bool(newValue))
                elif varType == 'int' and mod.Search.isInt(newValue):
                    settableValue = str(int(newValue))
                elif varType == 'float' and mod.Search.isFloat(newValue):
                    settableValue = str(float(newValue))
                
                if settableValue:
                    if isFrozen: mod.Loader.unfreezeVar(self._m1_vars__varName)
                    
                    if operator == 'append':
                        exec('renpy.store.'+settableVar.name+'.append('+settableValue+')')
                    else:
                        exec('renpy.store.'+settableVar.name+operator+settableValue)
                    return True
                else:
                    print("mod: No valid value for {} (varType: {})".format(settableVar.name, varType))
            except Exception as e:
                print("mod: Couldn't set value for "+settableVar.name+'. '+str(e))
                pass
            finally:
                if isFrozen: mod.Loader.freezeVar(self._m1_vars__varName)
            return False 
        
        def delete(self):
            try:
                
                currentValue = None
                namePath = self.namePath
                lastIndex = len(namePath)-1
                for index,currentPath in enumerate(namePath):
                    if index == 0:
                        if currentPath in self.storeDict:
                            if index == lastIndex: 
                                del self.storeDict[currentPath]
                                break
                            else:
                                currentValue = self.storeDict[currentPath]
                        else:
                            break 
                    else: 
                        if currentPath.startswith('.'): 
                            if hasattr(currentValue, currentPath[1:]):
                                if index == lastIndex: 
                                    delattr(currentValue, currentPath[1:])
                                    break
                                else:
                                    currentValue = getattr(currentValue, currentPath[1:])
                            else:
                                break
                        elif renpy.re.match(r"^\[[\"\'].+[\"\']\]$", currentPath): 
                            if currentPath[2:-2] in currentValue:
                                if index == lastIndex: 
                                    del currentValue[currentPath[2:-2]]
                                    break
                                else:
                                    currentValue = currentValue[currentPath[2:-2]]
                            else:
                                break
                        elif renpy.re.match(r"^\[\d+\]$", currentPath): 
                            currentIndex = int(currentPath[1:-1])
                            if isinstance(currentValue, list) and len(currentValue) > currentIndex:
                                if index == lastIndex: 
                                    del currentValue[currentIndex]
                                    break
                                else:
                                    currentValue = currentValue[currentIndex]
                            else:
                                break
            except Exception as e:
                print('mod: Failed to delete variable "{}": {}'.format(self.name, e))
                pass
        
        def getButtonValue(self, scalePercentage=None):
            """ Get a value to display on the result button """
            if self.varType in ['string', 'boolean', 'int', 'float']:
                val = str(self.value)
            elif self.varType == 'list':
                val = 'list ('+str(len(self.value))+' items)'
            elif self.varType == 'dict':
                val = 'dict ('+str(len(self.value))+' items)'
            else:
                val = self.varType
            
            if isinstance(val, basestring):
                if scalePercentage:
                    val = mod.scaleText(val.replace('\n', ' '), scalePercentage, 'mod_button_text')
            else:
                val = 'unknown type'
            
            return val
        
        def getChild(self, childVarName):
            if callable(childVarName): childVarName = childVarName()
            
            if self.varType in ['dict', 'list']:
                if isinstance(childVarName, int):
                    return modVar(self.name+'['+str(childVarName)+']')
                else:
                    return modVar(self.name+'["'+str(childVarName)+'"]')
            else:
                return modVar(self.name+'.'+str(childVarName))
        
        @property
        def children(self):
            if not hasattr(self, '__children'):
                self._m1_vars__children = []
                if self.varType == 'dict':
                    for key in self.value.keys():
                        self._m1_vars__children.append(self.getChild(key))
                elif self.varType == 'list':
                    for key in range(0, len(self.value)):
                        self._m1_vars__children.append(self.getChild(key))
                elif self.varType.startswith('<class '):
                    for key in self.value.__dict__.keys():
                        self._m1_vars__children.append(self.getChild(key))
            
            return self._m1_vars__children
        
        @staticmethod
        def getValType(val):
            import types
            
            try:
                if isinstance(val, basestring): 
                    return 'string'
                elif isinstance(val, bool): 
                    return 'boolean'
                elif isinstance(val, int): 
                    return 'int'
                elif isinstance(val, float): 
                    return 'float'
                elif isinstance(val, list): 
                    return 'list'
                elif isinstance(val, dict): 
                    return 'dict'
                elif isinstance(val, types.FunctionType):
                    return 'function'
                elif isinstance(val, renpy.python.StoreModule): 
                    return 'store'
                elif isinstance(val, renpy.persistent.Persistent): 
                    return 'persistent'
                elif isinstance(val, modSearchClass):
                    return 'modsearch'
                elif isinstance(val, renpy.python.StoreDeleted):
                    return 'deleted'
                elif hasattr(val, '__dict__'):
                    return str(type(val))
            except:
                pass
            
            return 'unknown'
        
        @staticmethod
        def getVarType(varName):
            try:
                val = eval(varName)
                return modVar.getValType(val)
            except:
                pass
            
            return 'unknown'
        
        @staticmethod
        def isSupportedVarType(varType):
            return varType in ['string', 'boolean', 'int', 'float', 'list', 'dict'] or varType.startswith('<class ')

    class modSetVarValue(NonPicklable):
        """ This class calls `setValue` on the passed `modVar` """
        def __init__(self, var, onSuccess, screenErrorVariable, *args, **kwargs):
            self.var = var
            self.onSuccess = onSuccess
            self.screenErrorVariable = screenErrorVariable
            self.args = args
            self.kwargs = kwargs
        
        def __call__(self):
            if self.var.setValue(*self.args, **self.kwargs):
                if callable(self.onSuccess):
                    self.onSuccess()
            elif self.screenErrorVariable:
                SetScreenVariable(self.screenErrorVariable, 'Unable to set variable, the value is probably invalid')()

    class modStoreMonitor(renpy.python.StoreDict):
        @staticmethod
        def init():
            try:
                if renpy.store.__dict__.__class__ == renpy.python.StoreDict:
                    renpy.store.__dict__.__class__ = modStoreMonitor
                    renpy.store.__dict__.originalClass = renpy.python.StoreDict 
                elif renpy.store.__dict__.__class__ != modStoreMonitor:
                    raise Exception('Unexpected store type: {}'.format(type(renpy.store.__dict__)))
                return True
            
            except Exception as e:
                print('mod: Failed to attach mod StoreMonitor: {}'.format(e))
                return False
        
        @staticmethod
        def isAttached():
            return (renpy.store.__dict__.__class__ == modStoreMonitor)
        
        def clear(self):
            
            self.__class__ = self.originalClass
            self.clear()
        
        def reset(self):
            
            self.__class__ = self.originalClass
            self.reset()
        
        def __setitem__(self, key, value):
            try:
                if mod.Loader.isFrozenVar(key):
                    return 
                
                if mod.Loader.isMonitoredVar(key):
                    if not renpy.get_screen('mod_modify_value') and value != self[key]: 
                        mod.Notifications.add(label='Variable changed', text=key, action=Show('mod_var_changed', varName=key, prevVal=self[key]))
            
            except Exception as e: 
                print('mod: Failed to handle change of value "{}". {}'.format(key, e))
            
            super(modStoreMonitor, self).__setitem__(key, value)
