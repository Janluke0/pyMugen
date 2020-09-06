#import configparser
from ..formats.utils.parser import parse 
from collections import namedtuple




class Character:
    def __init__(self,  directory):
        #TODO: something better
        self.directory = directory
        config = parse(f"{directory}/{directory}.def")
        self.info = {k:v for k,v in config.items("Info")}
        self.files = {k:v for k,v in config.items("Files")}
        self.arcade = {k:v for k,v in config.items("Arcade")}
        self._readfiles()

    def _readfiles(self):
        #cmd 
        #cns
        #st
        #stcommon #not in character directory

        #TODO: later
        #sprite
        #anim
        #sound
        #ai 
        pass
    
    @staticmethod
    def from_directory(path):
        pass
if False:
    c = Character('kfm')

    for ftype in c.files:
        if ftype != "sprite" and  ftype != "anim" and  ftype != "sound" and  ftype != "ai": #from mugen directory
            print(ftype)
            config = parse(f"{c.directory}/{c.files[ftype]}")
            for s in config.sections():
                for o in config[s]:
                    print(o, config[s][o])
                
            break
    