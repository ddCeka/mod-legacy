
init -1 python:

    class modSearchClass(NonPicklable):
        searchQuery = "" 
        searchRecursive = False 
        _m1_search__results = []
        _m1_search__itemsPerPage = 20
        _m1_search__currentPage = 1
        
        def __init__(self):
            self.queryInput = Input(autoFocus=not renpy.variant("touch"), onEnter=Function(self.doSearch))
        
        @property
        def lastLabel(self):
            """ Get last called label (note that ) """
            try:
                for rollback in reversed(renpy.game.log.log):
                    if isinstance(rollback.context.current, basestring):
                        return rollback.context.current
            except:
                pass
            return '(Unknown)'
        
        @property
        def results(self):
            return self._m1_search__results
        
        @property
        def pageCount(self):
            import math
            return int(math.ceil(len(self.results)/float(self._m1_search__itemsPerPage)))
        
        @property
        def pageRange(self):
            firstPage = mod.max(self.currentPage-3, 1)
            lastPage = mod.min(self.currentPage+3, self.pageCount)
            
            if firstPage == 1: 
                lastPage = mod.min(firstPage+6, self.pageCount) 
            elif lastPage == self.pageCount: 
                firstPage = mod.max(lastPage-6, 1) 
            
            return range(firstPage, lastPage+1)
        
        @property
        def pageStartIndex(self):
            return ((self._m1_search__currentPage-1)*self._m1_search__itemsPerPage)
        
        @property
        def pageEndIndex(self):
            return (self.pageStartIndex+self._m1_search__itemsPerPage)
        
        @property
        def currentPage(self):
            return self._m1_search__currentPage
        
        @currentPage.setter
        def currentPage(self, val):
            self._m1_search__currentPage = val
        
        @property
        def searchType(self):
            return mod.Settings.searchType
        
        @searchType.setter
        def searchType(self, newType):
            if mod.Settings.searchType == 'labels' or newType == 'labels': 
                self.resetSearch(keepInputQuery=True)
            mod.Settings.searchType = newType
        
        def doSearch(self):
            results = []
            self.searchQuery = str(self.queryInput)
            
            
            if renpy.variant('touch'): self.queryInput.Disable()()
            
            if len(self.searchQuery) > 0: 
                if mod.Settings.searchRecursive and len(self.results) > 0: 
                    varCollection = self.results
                    self.searchRecursive = True
                
                else: 
                    if self.searchType == 'labels':
                        varCollection = renpy.get_all_labels()
                    else:
                        varCollection = globals()
                    self.searchRecursive = False
                
                
                if self.searchType == 'variable names' or self.searchType == 'labels': 
                    for varName in varCollection:
                        if isinstance(varName, modVar):
                            matchedVarNames = self.matchVarName(varName.name, self.searchQuery)
                        else:
                            matchedVarNames = self.matchVarName(varName, self.searchQuery)
                        
                        if matchedVarNames:
                            results += matchedVarNames
                
                elif self.searchType == 'values': 
                    for varName in varCollection:
                        if isinstance(varName, modVar):
                            matchedVarNames = self.matchVarValue(varName.name, self.searchQuery)
                        else:
                            matchedVarNames = self.matchVarValue(varName, self.searchQuery)
                        
                        if matchedVarNames:
                            results += matchedVarNames
                
                self._m1_search__results = results
                self._m1_search__currentPage = 1
        
        def resetSearch(self, keepInputQuery=False):
            if not keepInputQuery: self.queryInput.set_text('')
            self.queryInput.Enable()()
            self.searchQuery = ''
            self._m1_search__results = []
            self.searchRecursive = False
            self._m1_search__currentPage = 1
        
        def _m1_search__getFullVarName(self, varName, parentVarName=None):
            """ Combine `varName` and `parentVarname` into one variable name """
            if parentVarName:
                if modVar.getVarType(parentVarName) == 'dict':
                    return parentVarName+'["'+str(varName)+'"]'
                else:
                    return parentVarName+'.'+str(varName)
            else:
                return varName
        
        def matchVarValue(self, varName, query, parentVarName=None):
            """
            Match a `varName`'s value with the `query`

            Returns: array of matched varNames (could be multiple variables if the supplied var is a list or dict)
            """
            fullVarName = self._m1_search__getFullVarName(varName, parentVarName)
            varType = modVar.getVarType(fullVarName)
            
            if not modVar.isSupportedVarType(varType): 
                return None
            
            elif varType == 'string':
                return [modVar(fullVarName)] if self._m1_search__matchStringValue(eval(fullVarName), query) else None
            
            elif varType == 'boolean' and (query.lower() == 'true' or query.lower() == 'false'):
                if eval(fullVarName): 
                    return [modVar(fullVarName)] if query.lower() == 'true' else None
                else: 
                    return [modVar(fullVarName)] if query.lower() == 'false' else None
            
            elif varType == 'int' and self.isInt(query):
                return [modVar(fullVarName)] if int(query) == eval(fullVarName) else None
            
            elif varType == 'float' and self.isFloat(query):
                return [modVar(fullVarName)] if float(query) == eval(fullVarName) else None
            
            elif varType == 'persistent' and mod.Settings.searchPersistent:
                varNames = []
                for subVarName in eval(fullVarName).__dict__.keys():
                    matchedVarNames = self.matchVarValue(subVarName, query, fullVarName)
                    if matchedVarNames:
                        varNames += matchedVarNames
                
                if len(varNames) > 0:
                    return varNames
            
            elif not parentVarName and mod.Settings.searchObjects and varType == 'dict': 
                varNames = []
                for subVarName in eval(fullVarName):
                    matchedVarNames = self.matchVarValue(subVarName, query, fullVarName)
                    if matchedVarNames:
                        varNames += matchedVarNames
                
                if len(varNames) > 0:
                    return varNames
            
            elif not parentVarName and mod.Settings.searchObjects and hasattr(eval(fullVarName), '__dict__'): 
                varNames = []
                for subVarName in eval(fullVarName).__dict__:
                    matchedVarNames = self.matchVarValue(subVarName, query, fullVarName)
                    if matchedVarNames:
                        varNames += matchedVarNames
                
                if len(varNames) > 0:
                    return varNames
        
        def matchVarName(self, varName, query, parentVarName=None):
            """
            Match a `varName` with the `query`

            Returns: array of matched varNames (could be multiple variables if the supplied var is a list, dict or object)
            """
            if not isinstance(varName, basestring):
                return
            
            fullVarName = self._m1_search__getFullVarName(varName, parentVarName)
            varType = 'label' if self.searchType == 'labels' else modVar.getVarType(fullVarName)
            
            if varType not in ['label','persistent'] and not modVar.isSupportedVarType(varType): 
                return None
            
            elif varType == 'persistent' and mod.Settings.searchPersistent:
                varNames = []
                for subVarName in eval(fullVarName).__dict__.keys():
                    matchedVarNames = self.matchVarName(subVarName, query, varName)
                    if matchedVarNames:
                        varNames += matchedVarNames
                
                if len(varNames) > 0:
                    return varNames
            
            elif not parentVarName and mod.Settings.searchObjects and varType == 'dict': 
                varNames = [modVar(varName)] if self._m1_search__matchStringValue(varName, query) else [] 
                for subVarName in eval(fullVarName).keys():
                    matchedVarNames = self.matchVarName(subVarName, query, fullVarName)
                    if matchedVarNames:
                        varNames += matchedVarNames
                
                if len(varNames) > 0:
                    return varNames
            
            elif not parentVarName and mod.Settings.searchObjects and varType != 'label' and hasattr(eval(fullVarName), '__dict__'): 
                varNames = [modVar(varName)] if self._m1_search__matchStringValue(varName, query) else [] 
                for subVarName in eval(fullVarName).__dict__.keys():
                    matchedVarNames = self.matchVarName(subVarName, query, fullVarName)
                    if matchedVarNames:
                        varNames += matchedVarNames
                
                if len(varNames) > 0:
                    return varNames
            
            else:
                return [modVar(fullVarName)] if self._m1_search__matchStringValue(varName, query) else None
        
        def _m1_search__matchStringValue(self, val, query):
            if mod.Settings.useWildcardSearch:
                import re
                query = re.escape(query)
                query = query.replace('\\*', '.*').replace('\\?', '.')
                query = '^{}$'.format(query)
                
                return bool(re.match(query, val, re.IGNORECASE))
            else:
                return (query.lower() in val.lower())
        
        def isInt(self, value):
            try:
                int(value)
                return True
            except:
                return False
        
        def isFloat(self, value):
            try:
                float(value)
                return True
            except:
                return False
