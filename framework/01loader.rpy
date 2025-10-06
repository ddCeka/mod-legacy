
init -999 python:
    class NonPicklable(python_object):
        
        def __setstate__(self, d):
            pass
        def __getstate__(self):
            return {}
        def __getnewargs__(self):
            return ()
        def __iter__(self):
            return None
        def itervalues(self):
            return None

    class Loader(NonPicklable):
        archiveFile = None
        
        @staticmethod
        def load_file(filename):
            if renpy.version_tuple[0] < 6 or (renpy.version_tuple[0] == 6 and (renpy.version_tuple[1] < 99 or (renpy.version_tuple[1] == 99 and renpy.version_tuple[2] < 14))):
                raise Exception("mod: Incompatible Ren'Py engine version")
            
            try:
                modFile = renpy.file(filename)
                inArchive = (renpy.android or modFile.name == None or modFile.name.endswith('.rpa'))
                
                if not inArchive: 
                    import hashlib, random, string
                    renpy.game.script.digest = hashlib.md5(''.join(random.choice(string.ascii_letters + string.digits) for i in range(20)).encode()) 
                elif hasattr(modFile, 'name'):
                    Loader.archiveFile = modFile.name
                
                loaded = (renpy.load_string(modFile.read().decode(), filename) != None)
                
            except:
                print(": Failed to load mod")
                raise 
