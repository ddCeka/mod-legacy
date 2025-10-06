
init 999 python:
    class modFontsHandler(NonPicklable):
        iconFont = 'FontAwesome5Free-Solid-900.otf'
        
        def __init__(self):
            if hasattr(config, 'font_transforms'):
                for font in config.font_transforms:
                    config.font_transforms[font] = self.createHandler(font, config.font_transforms[font])
        
        def createHandler(self, fontName, originalMethod):
            def handler(requestedFontName):
                if requestedFontName.endswith(modFontsHandler.iconFont):
                    return requestedFontName
                elif originalMethod:
                    return originalMethod(requestedFontName)
            
            return handler


    modFontsHandler()
