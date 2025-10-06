
init -1 python:

    class modLabel(NonPicklable):
        _m1_labels__instances = {}
        
        def __new__(self, labelName): 
            if not labelName in modLabel._m1_labels__instances:
                modLabel._m1_labels__instances[labelName] = modLabel._m1_labels__modLabel(labelName)
            return modLabel._m1_labels__instances[labelName]
        
        class _m1_labels__modLabel: 
            def __init__(self, labelName):
                self._m1_labels__labelName = labelName
                self._m1_labels__imageFileName = None
                self._m1_labels__image = {}
                self._m1_labels__imageDesaturated = {}
            
            @property
            def labelName(self):
                return self._m1_labels__labelName
            
            @property
            def imageFileName(self):
                if self.hasImage:
                    return self._m1_labels__imageFileName
            
            @property
            def hasImage(self):
                """ Check if we've found an image for this label """
                if self._m1_labels__imageFileName == '':
                    return False
                elif self._m1_labels__imageFileName != None:
                    return True
                else: 
                    self._m1_labels__imageFileName = '' 
                    try:
                        currentNode = renpy.game.script.lookup(self._m1_labels__labelName).next
                        for i in range(200): 
                            if not currentNode: 
                                break
                            else:
                                if hasattr(currentNode, 'imspec') and isinstance(currentNode.imspec[0], tuple): 
                                    image = renpy.display.image.images.get(currentNode.imspec[0])
                                    if image:
                                        filename = image.filename
                                        if renpy.loadable(filename): 
                                            self._m1_labels__imageFileName = filename
                                            return True
                                currentNode = currentNode.next 
                    except:
                        pass
                
                return False
            
            def getImage(self, width, height):
                """ Return a scaled image for this label. Returns `None` if no image is found """
                size = (width, height)
                if not size in self._m1_labels__image and self.hasImage: 
                    self._m1_labels__image[size] = renpy.display.im.Scale(self._m1_labels__imageFileName, width, height)
                
                if size in self._m1_labels__image:
                    return self._m1_labels__image[size]
            
            def getImageDesaturated(self, width, height):
                """ Return a scaled black and white image for this label. Returns `None` if no image is found """
                size = (width, height)
                if not size in self._m1_labels__imageDesaturated: 
                    image = self.getImage(width, height)
                    if image:
                        self._m1_labels__imageDesaturated[size] = renpy.display.im.MatrixColor(image, renpy.display.im.matrix.desaturate())
                
                if size in self._m1_labels__imageDesaturated:
                    return self._m1_labels__imageDesaturated[size]

    class modLabelImage(renpy.display.core.Displayable):
        
        def __init__(self, modLabel, desaturated=False):
            super(modLabelImage, self).__init__()
            self.modLabel = modLabel
            self.desaturated = desaturated
        
        def render(self, width, height, st, at):
            rv = renpy.display.render.Render(width, height)
            
            if self.modLabel.hasImage: 
                if self.desaturated:
                    imgRender = renpy.display.render.render(self.modLabel.getImageDesaturated(width, height), width, height, st, at)
                else:
                    imgRender = renpy.display.render.render(self.modLabel.getImage(width, height), width, height, st, at)
                rv.blit(imgRender, (0, 0))
            
            else: 
                if self.desaturated:
                    rv.fill(renpy.easy.color('#000'))
                else:
                    rv.fill(renpy.easy.color('#333'))
            
            return rv

    class modLabelMon(NonPicklable):
        def __init__(self):
            self._m1_labels__originalCallback = None
            self.lastLabel = None
            self.onLabelCalled = [] 
        
        def init(self):
            if config.label_callback:
                self._m1_labels__originalCallback = config.label_callback
            config.label_callback = self.labelCalled
        
        def labelCalled(self, label, called):
            for callback in self.onLabelCalled:
                callback(label, called)
            
            if not label.startswith('_') and label != 'after_load': 
                self.lastLabel = label
            
            
            if self._m1_labels__originalCallback:
                self._m1_labels__originalCallback(label, called)
