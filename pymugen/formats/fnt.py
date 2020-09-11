import ctypes
from .images.pcx import read_stream
"""
/*--| FNT file structure |--------------------------------------------------*\
/*
 * Very simple file format, formed by concatenating a pcx file and a text
 * file together and prepending a header.
 * May be optimized for size by stripping the text file of comments before
 * adding it to the .fnt file. Be sure text data comes last in the file.
 */

  Version 1.0
HEADER
------
Bytes
00-11  "ElecbyteFnt\0" signature                                         [12]
12-15  2 verhi, 2 verlo                                                  [04]
16-20  File offset where PCX data is located.                            [04]
20-23  Length of PCX data in bytes.                                      [04]
24-27  File offset where TEXT data is located.                           [04]
28-31  Length of TEXT data in bytes.                                     [04]
32-63  Blank; can be used for comments.                                  [40]
\*--------------------------------------------------------------------------*/

"""
class FntHeader(ctypes.Structure):
    _fields_ = [
        ('signature', ctypes.ARRAY(ctypes.c_uint8,12)),    
        ('verlo0',ctypes.c_uint8),
        ('verhi0',ctypes.c_uint8),
        ('verhi1',ctypes.c_uint8),
        ('verlo1',ctypes.c_uint8),   

        ('pcx_offset',ctypes.c_uint32),

        ('txt_offset',ctypes.c_uint32),
        ('txt_len',ctypes.c_uint32),
        ('BLANK', ctypes.ARRAY(ctypes.c_char,40))
    ]
    _pcx = None
    _conf = None
    def __repr__(self): 
        out = f"{self.__class__.__name__}("
        for k,_ in self._fields_:
            out += f"{k}={getattr(self, k)}, "
        return out[:-2] + ")"

def parse(conf):
    res = {}
    p = None
    for l in conf.splitlines():
        if l.strip().startswith(";") or l.strip()=="":
            continue
        elif  l.startswith("["):
            n = l.split("[")[1].split("]")[0].lower()
            res[n] = {}
            p = res[n] 
        else:
            if "=" in l:
                k,v = l.strip().split("=")
                if ',' in v:
                    v = (*[int(n) for n in v.strip().split(',')],)
                p[k.strip().lower()] = v
            else:
                t = [v.strip() for v in l.strip().split()]
                if '0x' in t[0]:
                   t[0] =  bytes.fromhex(t[0].replace('0x','')).decode('ascii')
                p[t[0]] = int(t[1]), int(t[2])
    return res

def from_file(fname):
    with open(fname,"rb") as fp:
        bf = fp.read(ctypes.sizeof(FntHeader))
        f = FntHeader.from_buffer_copy(bf)
        #print(f)
        fp.seek(f.pcx_offset)
        f._pcx = read_stream(fp)
        skip = 64 #????????????
        fp.seek(f.txt_offset+skip)
        f._conf = parse(fp.read(f.txt_len-skip).decode('utf-8'))
    return f

