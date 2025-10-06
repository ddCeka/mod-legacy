
init -1 python:

    class modTextReplacement(NonPicklable):
        def __init__(self, original, replacement, characterVar=None, caseInsensitive=False, replacePartialWords=False):
            self.original = original if not callable(original) else original()
            self.replacement = replacement if not callable(replacement) else replacement()
            self.characterVar = characterVar if not callable(characterVar) else characterVar()
            self.caseInsensitive = caseInsensitive if not callable(caseInsensitive) else caseInsensitive()
            self.replacePartialWords = replacePartialWords if not callable(replacePartialWords) else replacePartialWords()
        
        def __call__(self, text):
            import re
            
            if self.characterVar: 
                char = eval(self.characterVar)
                if isinstance(char, ADVCharacter) and hasattr(char, 'dynamic') and char.dynamic: 
                    text = text.replace('[{}]'.format(self.characterVar), self.replacement)
                    text = text.replace('[{}]'.format(self.original), self.replacement)
            
            if self.original[:1] == '[' and self.original[-1:] == ']': 
                text = text.replace(self.original, self.replacement)
            else:
                if self.replacePartialWords:
                    replacement = re.compile(re.escape(self.original), re.IGNORECASE if self.caseInsensitive else 0)
                else:
                    replacement = re.compile('\\b{}(?!\\w)'.format(re.escape(self.original)), re.IGNORECASE if self.caseInsensitive else 0) 
                text = replacement.sub(self.replacement, text)
            
            return text

    class modTextReplacementsClass(NonPicklable):
        _m1_textrepl__itemsPerPage = 20
        _m1_textrepl__currentPage = 1
        
        def __init__(self):
            self.replacements = modOrderedDict()
            self._m1_textrepl__characters = None
            self._m1_textrepl__defaultTextFilter = None
            self._m1_textrepl__defaultSayFilter = None
        
        @property
        def pageCount(self):
            import math
            return int(math.ceil(len(self.replacements)/float(self._m1_textrepl__itemsPerPage)))
        
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
            return ((self._m1_textrepl__currentPage-1)*self._m1_textrepl__itemsPerPage)
        
        @property
        def pageEndIndex(self):
            return (self.pageStartIndex+self._m1_textrepl__itemsPerPage)
        
        @property
        def currentPage(self):
            if self.pageStartIndex > len(self.replacements): 
                self._m1_textrepl__currentPage = 1
            
            return self._m1_textrepl__currentPage
        
        @currentPage.setter
        def currentPage(self, val):
            self._m1_textrepl__currentPage = val
        
        class AddReplacement(NonPicklable):
            def __init__(self, *args, **kwargs):
                self.args = args
                self.kwargs = kwargs
            
            def __call__(self):
                mod.TextRepl.addReplacement(modTextReplacement(*self.args, **self.kwargs))
        
        def addReplacement(self, textReplacement):
            """ Add or update a replacement """
            self.replacements[textReplacement.original] = textReplacement
            mod.Loader.unsavedChanges = True
        
        def delReplacement(self, original):
            if original in self.replacements:
                del self.replacements[original]
                mod.Loader.unsavedChanges = True
        
        def clearReplacements(self):
            self.replacements = modOrderedDict()
        
        def changePos(self, sourceReplOriginal, targetReplOriginal):
            if sourceReplOriginal in self.replacements and targetReplOriginal in self.replacements:
                self.replacements.changePos(sourceReplOriginal, targetReplOriginal)
                self.unsavedChanges = True
        
        def sortReplacements(self, reverse=False, sortReplacement=False):
            self.replacements.sort(reverse, sortByAttr=('replacement' if sortReplacement else None))
            self.unsavedChanges = True
        
        def attachFilters(self):
            if not self.incompatible:
                if config.say_menu_text_filter != self._m1_textrepl__textFilter: 
                    self._m1_textrepl__defaultTextFilter = config.say_menu_text_filter
                    config.say_menu_text_filter = self._m1_textrepl__textFilter
                
                if config.say_arguments_callback != self._m1_textrepl__sayFilter: 
                    self._m1_textrepl__defaultSayFilter = config.say_arguments_callback
                    config.say_arguments_callback = self._m1_textrepl__sayFilter
        
        @property
        def incompatible(self):
            return not hasattr(config, 'say_arguments_callback')
        
        @property
        def characters(self):
            if(self._m1_textrepl__characters == None):
                self._m1_textrepl__characters = []
                for key,value in renpy.store.__dict__.items():
                    if isinstance(value, ADVCharacter):
                        self._m1_textrepl__characters.append(key)
            
            return self._m1_textrepl__characters
        
        def _m1_textrepl__textFilter(self, text):
            if self._m1_textrepl__defaultTextFilter:
                text = self._m1_textrepl__defaultTextFilter(text)
            
            for original,replacement in self.replacements.items():
                text = replacement(text)
            
            return text
        
        def _m1_textrepl__sayFilter(self, who, *args, **kwargs):
            if self._m1_textrepl__defaultSayFilter:
                args, kwargs = self._m1_textrepl__defaultSayFilter(who, *args, **kwargs)
            
            if isinstance(who, basestring):
                if who in self.replacements and self.replacements[who].characterVar:
                    kwargs['name'] = self.replacements[who](who)
            elif isinstance(who, ADVCharacter) and hasattr(who, 'name') and isinstance(who.name, basestring):
                if who.name in self.replacements and self.replacements[who.name].characterVar:
                    if hasattr(who, 'dynamic') and who.dynamic:
                        kwargs['name'] = repr(self.replacements[who.name](who.name))
                    else:
                        kwargs['name'] = self.replacements[who.name](who.name)
            
            return args, kwargs


init 999 python:

    mod.TextRepl.attachFilters()
