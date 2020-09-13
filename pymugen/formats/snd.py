import ctypes
import io
import wave

from ._base import AbstractFormat
"""
/*--| SND file structure
|--------------------------------------------------*\
  Version 1.01
HEADER
------
Bytes
00-11  "ElecbyteSnd\0" signature				[12]
12-15  4 verhi, 4 verlo						[04]
16-19  Number of sounds						[04]
20-23  File offset where first subfile is located.		[04]
24-511 Blank; can be used for comments.				[488]
"""
class SndHeader(ctypes.Structure):
    _fields_ = [
        ('signature', ctypes.ARRAY(ctypes.c_uint8,12)),    
        ('verlo0',ctypes.c_uint8),
        ('verhi0',ctypes.c_uint8),
        ('verhi1',ctypes.c_uint8),
        ('verlo1',ctypes.c_uint8),   

        ('sounds_count',ctypes.c_uint32),

        ('first_subheader_offset',ctypes.c_uint32),
        ('BLANK', ctypes.ARRAY(ctypes.c_uint8,488))
    ]
    def __repr__(self): 
        out = f"{self.__class__.__name__}("
        for k,_ in self._fields_:
            out += f"{k}={getattr(self, k)}, "
        return out[:-2] + ")"

"""
SUBFILEHEADER
-------
Bytes
00-03 File offset where next subfile in the linked list is	[04]
      located. Null if last subfile.
04-07 Subfile length (not including header.)			[04]
08-11 Group number						[04]
12-15 Sample number						[04]
08-   Sound data (WAV)

"""

class SndSubHeader(ctypes.Structure):
    _fields_ = [
        ('next_subheader_offset',ctypes.c_uint32),
        ('length',ctypes.c_uint32),
        ('group_num',ctypes.c_uint32),
        ('sound_num',ctypes.c_uint32),
    ]
    _wave = None
    @property
    def wave(self):
        return  wave.open(self._wave)

    @wave.setter
    def wave(self, wav):
        if type(wav) is wave.Wave_read:
            self._wave = io.BytesIO()
            dst = wave.open(self._wave,"wb")
            dst.setparams(wav.getparams())
            dst.writeframes(wav.readframes(wav.getnframes()))
            dst.close()
            self._wave.seek(0)
           
        else:
            raise ValueError()

    def __repr__(self): 
        out = f"{self.__class__.__name__}("
        for k,_ in self._fields_:
            out += f"{k}={getattr(self, k)}, "
        return out[:-2] + ")"



class Snd(AbstractFormat):
    _max_keys = 2 #group and number
    _formats_avaible = ["snd"]
    def __init__(self, source, *args, **kwargs):
        super().__init__(source, encoding=None, read_mode="rb", write_mode="wb", *args, **kwargs)
        if self._data is None:
            self._data = [None,[]] 

    def get_item(self, group, num):
        for s in self._data[1]:
            if s.group_num == group and s.sound_num == num:
                return s.wave 
        raise IndexError()

    def set_item(self, index, value=None):
        #TODO
        #if new update file header
        pass
   
    def get_keys(self):
        group_nums = {s.group_num for s in self._data[1]}
        groups = {}
        for gn in group_nums:
            groups[gn] = [s.sound_num for s in self._data if s.group_num == gn]
        return groups
   
    def _read(self):
        self._data = [None,[]] 
        buf = self._buff.read(ctypes.sizeof(SndHeader))
        h = SndHeader.from_buffer_copy(buf)
        self._buff.seek(h.first_subheader_offset)
        buf = self._buff.read(ctypes.sizeof(SndSubHeader))
        self._data[0] = h
        while buf:
            sh = SndSubHeader.from_buffer_copy(buf)
            sh.wave = wave.open(self._buff)
            self._data[1].append(sh)
            self._buff.seek(sh.next_subheader_offset)
            buf = self._buff.read(ctypes.sizeof(SndSubHeader))


    def _write(self, _format):
        #TODO
        pass

class _Snd:
    def __init__(self, fname):
        super().__init__()
        self._sounds = from_file(fname)

    def get_sound(self, group, num):
        for s in self._sounds:
            if s.group_num == group and s.sound_num == num:
                return s.wave
        return None


    @property
    def groups(self):
        group_nums = {s.group_num for s in self._sounds}
        groups = {}
        for gn in group_nums:
            groups[gn] = [s.sound_num for s in self._sounds if s.group_num == gn]
        return groups