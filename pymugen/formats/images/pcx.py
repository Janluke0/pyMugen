import ctypes
from collections import namedtuple
import os
import numpy as np
class RGB(ctypes.Structure):
    _fields_ = [
        ('r', ctypes.c_uint8),
        ('g', ctypes.c_uint8),
        ('b', ctypes.c_uint8),
    ]
    def __repr__(self): 
        out = f"{self.__class__.__name__}("
        for k,_ in self._fields_:
            out += f"{k}={getattr(self, k)}, "
        return out[:-2] + ")"


class PCXHeader(ctypes.Structure):
    _fields_ = [('Manufacturer', ctypes.c_uint8),
                ('version', ctypes.c_uint8),
                ('Encoding', ctypes.c_uint8),
                ('BPP', ctypes.c_uint8), #bits per pixel
                
                ('x_min', ctypes.c_uint16),
                ('y_min', ctypes.c_uint16),
                ('x_max', ctypes.c_uint16),
                ('y_max', ctypes.c_uint16),
                ('Hdpi', ctypes.c_uint16),
                ('Vdpi', ctypes.c_uint16), #16B

                ('ColorMap', ctypes.ARRAY(RGB,16)),
                ('reserved', ctypes.c_uint8),
                ('NPlanes', ctypes.c_uint8),
                ('BytesPerLine', ctypes.c_uint16),
                ('paletteInfo', ctypes.c_uint16),

                ('Hscreen_res', ctypes.c_uint16),
                ('Vscreen_res', ctypes.c_uint16),
                
                ('reserved2', ctypes.ARRAY(ctypes.c_uint8,54))
    ]
    @property
    def width(self):
        return self.x_max - self.x_min +1

    @property
    def height(self):
        return self.y_max - self.y_min +1

    @property
    def is_compressed(self):
        return self.Encoding == 1
    
    def __repr__(self): 
        out = f"{self.__class__.__name__}("
        for k,_ in self._fields_:
            out += f"{k}={getattr(self, k)}, "
        return out[:-2] + ")"


def read_img8(f, header):
    img = np.zeros((header.width, header.height), dtype=np.uint8)
    for y in range(header.height):
        line = read_line(f,header, header.BytesPerLine)
        for x in range(header.width):
           img[x,y] = line[x]
        #img[:,y] = line
    img = np.rot90(img,-1)
    img = np.fliplr(img)
    palette = np.empty((256,3), dtype=np.uint8)
    b = f.read(1)
    flag = int.from_bytes(b,'big')
    if flag == 12 and ( header.version == 5 or header.version == 2):
        #read palette
        for x in range(256):
            palette[x,0] = int.from_bytes(f.read(1),'big')
            palette[x,1] = int.from_bytes(f.read(1),'big')
            palette[x,2] = int.from_bytes(f.read(1),'big')
    else:
        print("ELSE")
    return img, palette

def read_img24(f, header):
    img = np.empty((header.width, header.height, 3), dtype=np.uint8)
    for y in range(header.height):
        img[y,:,0] = read_line(f, header, header.BytesPerLine)
        img[y,:,1] = read_line(f, header, header.BytesPerLine)
        img[y,:,2] = read_line(f, header, header.BytesPerLine)
    return img

def read_img1(f, header):
    raise NotImplementedError()

def read_img4(f, header):
    raise NotImplementedError()

def read_line(f, header, size):
    img = np.empty(size)#, dtype=np.uint8)
    i = 0
    if header.is_compressed:
        while i < size:
            c = 1
            b = f.read(1)
            if b > b'\xc0':
                c = int.from_bytes(b,'big') - 0xc0
                b = f.read(1)
            while c and i < size:
                img[i] = int.from_bytes(b,'big') 
                i += 1
                c -= 1
    else:
        while i < size:
            b = f.read(1)
            img[i] = b
            i += 1
    return img

def read_file(fname):
    #tot = os.stat(fname).st_size
    with open(fname,"rb") as fp:
        return read_stream(fp)

def read_stream(fp, return_header=False):
    header = PCXHeader.from_buffer_copy(
                    fp.read(ctypes.sizeof(PCXHeader))
                )
    # print(header)
    assert header.Manufacturer == 10
    if header.BPP == 1 and header.NPlanes == 1:
        img, pal = read_img1(fp, header)
    elif header.BPP == 1 and header.NPlanes == 4:
        img, pal = read_img4(fp, header)
    elif header.BPP == 8 and header.NPlanes == 1:
        img, pal = read_img8(fp, header)
    elif header.BPP == 8 and header.NPlanes == 3:
        img, pal = read_img24(fp, header), None
    else:
        raise NotImplementedError()
    ##DEBUG
    #for f,_ in PCXHeader._fields_:
    #    if f == "ColorMap":
    #        print(f, "=", [v for v in getattr(header,f)])
    #    else:
    #        print(f, "=", getattr(header,f))
    #DEBUG
    #if pal is not None:
    #    pal = pal[::-1]

    if return_header:
        return img, pal, header  
        
    return img, pal   

