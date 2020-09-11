from ..formats.utils.parser import parse 
from ..formats import cns, air, sff, snd
from collections import namedtuple
import pathlib,os


ENCODING = 'latin-1'
class Character:
    def __init__(self,  dir_path, def_fname):
        #TODO: something better
        self.directory = pathlib.Path(dir_path).absolute()
        self._raw_config = parse(self.directory / f"{def_fname}.def")

        self.files = {k:v for k,v in self._raw_config["Files"].items()}  #mandatory
        self.info = {k:v for k,v in self._raw_config["Info"].items()}  if "Info" in self._raw_config else None
        self.arcade = {k:v for k,v in self._raw_config["Arcade"].items()} if "Arcade" in self._raw_config else None
        self._readfiles()

    def _readfiles(self):
        #cmd
        # TODO 
        #cns
        self._cns = cns.parse_cns(self.directory / self.files["cns"], ENCODING)
        #st
        self._st = cns.parse_cns(self.directory / self.files["st"], ENCODING)
        #stcommon 
        # TODO
        #sprite
        self._sff = sff.SFF(self.directory / self.files["sprite"])
        #anim
        self._air = air.from_file(self.directory / self.files["anim"], ENCODING)
        #sound
        self._snd = snd.Snd(self.directory / self.files["sound"])
        #ai 
        pass
    
    @staticmethod
    def from_directory(path):
        pass


