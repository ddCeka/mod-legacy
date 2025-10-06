
init -1 python:

    class modGameSaves(NonPicklable):
        
        def slotTime(self, slot, empty='(no time)'):
            import time
            
            mtime = renpy.slot_mtime(slot)
            if not mtime:
                return empty
            else:
                return time.strftime('%a, %b %d %Y, %H:%M', time.localtime(mtime))
        
        def slotName(self, slot, empty=''):
            json = renpy.slot_json(slot)
            
            if not json:
                return empty
            else:
                return json.get('_save_name', empty) or empty
        
        def load(self, slot):
            if renpy.can_load(slot):
                mod.Confirm('Do you want to load this save? Unsaved progress will be lost', Function(renpy.load, slot), title='Load save')()
        
        class Save(NonPicklable):
            def __init__(self, *args, **kwargs):
                self.args = args
                self.kwargs = kwargs
            
            def __call__(self):
                mod.Gamesaves.save(*self.args, **self.kwargs)
        
        def save(self, slot, name=None, overwrite=False, notify=False):
            if name == None and mod.Settings.askSaveName:
                def callback(saveName):
                    if callable(saveName): saveName = saveName()
                    
                    self.save(slot, saveName, overwrite, notify)
                
                renpy.show_screen('mod_gamesaves_savename', callback)
            else:
                if not overwrite and renpy.can_load(slot):
                    mod.Confirm('Do you want to overwrite the existing save?', Function(self.save, slot, name or '', overwrite=True, notify=notify), title='Overwrite save')()
                else:
                    renpy.save(slot, name or '')
                    if notify:
                        if isinstance(notify, basestring):
                            renpy.notify(notify)
                        else:
                            renpy.notify('Game saved')
        
        
        def delete(self, slot):
            if renpy.can_load(slot):
                mod.Confirm('Are you sure you want to delete this save?', Function(renpy.unlink_save, slot), title='Delete save')()
        
        def copy(self, sourceSlot, destSlot=None):
            if not destSlot:
                def callback(page, position):
                    if callable(page): page = page()
                    if callable(position): position = position()
                    
                    if not mod.Search.isInt(page) or not mod.Search.isInt(position):
                        mod.Confirm('The page/position is invalid, please input numeric values', title='Invalid slot')()
                    else:
                        self.copy(sourceSlot, '{}-{}'.format(page, position))
                
                renpy.show_screen('mod_gamesaves_selectslot', sourceSlot.split('-')[0], sourceSlot.split('-')[1], callback, 'Copy')
            
            elif renpy.can_load(destSlot):
                mod.Confirm('Do you want to overwrite the existing save in the destination slot?', Function(renpy.copy_save, sourceSlot, destSlot), title='Overwrite save')()
            
            else:
                renpy.copy_save(sourceSlot, destSlot)
        
        def move(self, sourceSlot, destSlot=None):
            if not destSlot:
                def callback(page, position):
                    if callable(page): page = page()
                    if callable(position): position = position()
                    
                    if not mod.Search.isInt(page) or not mod.Search.isInt(position):
                        mod.Confirm('The page/position is invalid, please input numeric values', title='Invalid slot')()
                    else:
                        self.move(sourceSlot, '{}-{}'.format(page, position))
                
                renpy.show_screen('mod_gamesaves_selectslot', sourceSlot.split('-')[0], sourceSlot.split('-')[1], callback, 'Move')
            
            elif renpy.can_load(destSlot):
                mod.Confirm('Do you want to overwrite the existing save in the destination slot?', Function(renpy.rename_save, sourceSlot, destSlot), title='Overwrite save')()
            
            else:
                renpy.rename_save(sourceSlot, destSlot)
        
        class SetPage(NonPicklable):
            def __init__(self, page):
                self.page = page
            
            def __call__(self):
                page = self.page if not callable(self.page) else self.page()
                mod.Gamesaves.page = page
        
        @property
        def page(self):
            page = persistent._file_page
            if mod.Search.isInt(page):
                return int(page)
            else:
                return page
        
        @page.setter
        def page(self, val):
            if val == 'auto' or val == 'quick' or mod.Search.isInt(val):
                persistent._file_page = val
        
        @property
        def prevPage(self):
            page = self.page
            if page == 'auto':
                return 'auto'
            elif page == 'quick':
                return 'auto'
            elif page == 1:
                return 'quick'
            else:
                return page-1
        
        @property
        def nextPage(self):
            page = self.page
            if page == 'auto':
                return 'quick'
            elif page == 'quick':
                return 1
            else:
                return page+1
        
        @property
        def pageRange(self):
            page = self.page
            if not mod.Search.isInt(page):
                return range(1, 8)
            else:
                firstPage = mod.max(page-3, 1)
                lastPage = page+3
                
                if firstPage == 1: 
                    lastPage = firstPage+6 
                
                return range(firstPage, lastPage+1)
        
        class SetPageName(NonPicklable):
            def __init__(self, pageName):
                self.pageName = pageName
            
            def __call__(self):
                pageName = self.pageName if not callable(self.pageName) else self.pageName()
                mod.Gamesaves.pageName = pageName
        
        @property
        def pageName(self):
            page = self.page
            if page == "auto":
                return 'Auto save'
            elif page == "quick":
                return 'Quick save'
            else:
                default = 'Page {}'.format(page)
                pageName = persistent._file_page_name.get(page, default)
                return pageName.strip() or default
        
        @pageName.setter
        def pageName(self, val):
            page = self.page
            if page == 'auto' or page == 'quick':
                return
            else:
                if not val:
                    persistent._file_page_name.pop(page, None)
                else:
                    persistent._file_page_name[page] = val
        
        class SlotScreenshot(renpy.display.core.Displayable):
            
            def __init__(self, slot):
                super(modGameSaves.SlotScreenshot, self).__init__()
                self.slot = slot
            
            def render(self, width, height, st, at):
                rv = renpy.display.render.Render(width, height)
                
                img = renpy.display.im.MatrixColor(renpy.slot_screenshot(self.slot), renpy.display.im.matrix.opacity(.9))
                imgRender = renpy.display.render.render(renpy.display.im.Scale(img, width, height), width, height, st, at)
                rv.blit(imgRender, (0, 0))
                
                return rv
