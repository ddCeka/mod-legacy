
init -1 python:

    class modPages(NonPicklable):
        def __init__(self, itemCount, itemsPerPage=20):
            self.itemCount = itemCount
            self.itemsPerPage = itemsPerPage
            self._m1_pages__currentPage = 1
        
        @property
        def pageCount(self):
            import math
            return int(math.ceil(self.itemCount/float(self.itemsPerPage)))
        
        @property
        def pageStartIndex(self):
            return ((self.currentPage-1)*self.itemsPerPage)
        
        @property
        def pageEndIndex(self):
            return (self.pageStartIndex+self.itemsPerPage)
        
        @property
        def currentPage(self):
            return mod.min(self._m1_pages__currentPage, self.pageCount)
        
        @currentPage.setter
        def currentPage(self, val):
            self._m1_pages__currentPage = val
        
        @property
        def pageRange(self):
            firstPage = mod.max(self.currentPage-3, 1)
            lastPage = mod.min(self.currentPage+3, self.pageCount)
            
            if firstPage == 1: 
                lastPage = mod.min(firstPage+6, self.pageCount) 
            elif lastPage == self.pageCount: 
                firstPage = mod.max(lastPage-6, 1) 
            
            return range(firstPage, lastPage+1)
