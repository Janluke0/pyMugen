import ctypes
from collections import namedtuple

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
    @property
    def wave(self):
        return self._params, self._frames

    @wave.setter
    def wave(self, wav):
        self._params = wav.getparams()
        self._frames = wav.readframes(self._params[3])

    def __repr__(self): 
        out = f"{self.__class__.__name__}("
        for k,_ in self._fields_:
            out += f"{k}={getattr(self, k)}, "
        return out[:-2] + ")"

import wave
def from_file(fname):
    sounds = []
    with open(fname, "rb") as fp:
        buf = fp.read(ctypes.sizeof(SndHeader))
        h = SndHeader.from_buffer_copy(buf)
        fp.seek(h.first_subheader_offset)
        buf = fp.read(ctypes.sizeof(SndSubHeader))
        while buf:
            sh = SndSubHeader.from_buffer_copy(buf)
            sh.wave = wave.open(fp)
            sounds.append(sh)
            """
            print( "Number of channels",wav.getnchannels())
            print ( "Sample width",wav.getsampwidth())
            print ( "Frame rate.",wav.getframerate())
            print ("Number of frames",wav.getnframes())
            print ( "parameters:",wav.getparams())
            print(sh, wav)# len(wav_buf), wav_buf[:12])
            """
            fp.seek(sh.next_subheader_offset)
            buf = fp.read(ctypes.sizeof(SndSubHeader))
    return sounds


class Snd:
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