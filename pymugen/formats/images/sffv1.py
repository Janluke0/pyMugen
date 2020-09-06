import ctypes
from .pcx import read_stream
from collections import namedtuple

class SFFHeader(ctypes.Structure):
    _fields_ = [('signature', ctypes.ARRAY(ctypes.c_char,12)),
                ('verhi', ctypes.c_uint8),
                ('verlo', ctypes.c_uint8),
                ('verlo2', ctypes.c_uint8),
                ('verlo3', ctypes.c_uint8),
                ('num_groups', ctypes.c_long),
                ('num_images', ctypes.c_long),
                ('first_offset', ctypes.c_long),
                ('subheader_size', ctypes.c_long),
                ('is_shared', ctypes.c_bool),
                ('reserved', ctypes.ARRAY(ctypes.c_uint8,3)),
                ('BLANK', ctypes.ARRAY(ctypes.c_uint8,476))]    
    def __repr__(self): 
        out = f"{self.__class__.__name__}("
        for k,_ in self._fields_:
            out += f"{k}={getattr(self, k)}, "
        return out[:-2] + ")"

class SFFSpriteHeader(ctypes.Structure):
    _fields_ = [
        ('offset_next_sprite', ctypes.c_long),
        ('subfile_len', ctypes.c_long),
        ('x', ctypes.c_short),
        ('y', ctypes.c_short),
        ('groupno', ctypes.c_short),
        ('imageno', ctypes.c_short),
        ('linked', ctypes.c_short),
        ('is_shared', ctypes.c_bool),
        ('BLANK', ctypes.ARRAY(ctypes.c_uint8,13))
    ]   
    image, palette_index = None, None
    def __repr__(self): 
        out = f"{self.__class__.__name__}("
        for k,_ in self._fields_:
            out += f"{k}={getattr(self, k)}, "
        return out[:-2] + ")"

SFFPalette = namedtuple("SFFPalette",["group","n","data"])



def from_file(fname, progress_cb=None, def_palette_index=0):
    sprites = []
    palettes = []
    pal_index = []
    with open(fname, "rb") as fp:
        buf = fp.read(ctypes.sizeof(SFFHeader))
        header = SFFHeader.from_buffer_copy(buf)
        assert header.signature == b'ElecbyteSpr'  
        print(header)      
        assert header.verhi == 0 and header.verlo == 1 
        assert header.verlo2 == 0 and header.verlo3 == 1
        last_pal = None
        fp.seek(header.first_offset)
        buf = fp.read(ctypes.sizeof(SFFSpriteHeader))
        for _ in range(header.num_images):
            sprh = SFFSpriteHeader.from_buffer_copy(buf)
            if sprh.linked == 0:
                img, pal, pcx_h = read_stream(fp, True)
                if not sprh.is_shared:
                    palettes.append(SFFPalette(
                        sprh.groupno,
                        sprh.imageno,
                        pal
                    ))
                    if ((sprh.groupno == 9000 and sprh.imageno == 0) or
                        (sprh.groupno == 0 and sprh.imageno == 0)):
                        pal_index = def_palette_index
                    else:
                        pal_index = len(palettes) - 1
                else:
                    if ((sprh.groupno == 9000 and sprh.imageno == 0) or
                        (sprh.groupno == 0 and sprh.imageno == 0)):
                        pal_index = def_palette_index
                sprh.image = img
                sprh.palette_index = pal_index
                sprh.palette = pal # redundant

            sprites.append(sprh)

            if progress_cb is not None:
                progress_cb(len(sprites),header.num_images)
            
            fp.seek(sprh.offset_next_sprite)
            buf = fp.read(ctypes.sizeof(SFFSpriteHeader))

    for sprh in sprites:
        if sprh.linked != 0:
            t = sprites[sprh.linked]
            sprh.image = t.image
            sprh.palette_index = t.palette_index
        
    return sprites, header, palettes