import ctypes

""" NOMEN
struct _SFFV2_SFF_HEADER {
  char signature[12];
  quint8 verlo3; //0
  quint8 verlo2; //0
  quint8 verlo1; //0
  quint8 verhi;  //2
  char reserved1[4]; //4 bytes = 0	
  char reserved2[4]; //4 bytes = 0
  
  quint8 compatverlo3; //0
  quint8 compatverlo2; //0
  quint8 compatverlo1; //0
  quint8 compatverhi; //2
  char reserved3[4];
  char reserved4[4];
  
  long first_sprnode_offset;
  long total_frames;
  long first_palnode_offset;
  long total_palettes;
  long ldata_offset;
  long ldata_length;
  long tdata_offset;
  long tdata_length;
  char reserved5[4]; //4 bytes = 0
  char reserved6[4]; //4 bytes = 0
  char unused[436]; //436 bytes = 0
};
"""
class SFFHeader(ctypes.Structure):
    _fields_ = [
        ('signature', ctypes.ARRAY(ctypes.c_uint8,11)),
        ('verlo3',ctypes.c_uint8),
        ('verlo2',ctypes.c_uint8),
        ('verlo1',ctypes.c_uint8),
        ('verhi',ctypes.c_uint8),

        ('reserved1', ctypes.ARRAY(ctypes.c_uint8,4)),
        ('reserved2', ctypes.ARRAY(ctypes.c_uint8,4)),
        
        ('compatverlo3',ctypes.c_uint8),
        ('compatverlo2',ctypes.c_uint8),
        ('compatverlo1',ctypes.c_uint8),
        ('compatverhi',ctypes.c_uint8),

        ('reserved3', ctypes.ARRAY(ctypes.c_uint8,4)),
        ('reserved4', ctypes.ARRAY(ctypes.c_uint8,4)),

        ('first_sprnode_offset', ctypes.c_long),
        ('total_frames', ctypes.c_long),
        ('first_palnode_offset', ctypes.c_long),
        ('total_palettes', ctypes.c_long),
        ('ldata_offset', ctypes.c_long),
        ('ldata_length', ctypes.c_long),
        ('tdata_offset', ctypes.c_long),
        ('tdata_length', ctypes.c_long),
        
        ('reserved5', ctypes.ARRAY(ctypes.c_uint8,4)),
        ('reserved6', ctypes.ARRAY(ctypes.c_uint8,4)),

        ('BLANK', ctypes.ARRAY(ctypes.c_uint8,436))
    ]   
"""

struct _SFFV2_SPRITE_NODE_HEADER {
  short groupno;
  short imageno;
  short w; //dimensioni immagini: w
  short h; //dimensioni immagini: h
  short x;
  short y;
  short linked;
  quint8 fmt; //0=raw, 1=invalid, 2=RLE8, 3=RLE5, 4=LZ5
  quint8 colordepth;
  long offset; //offset into ldata or tdata
  long len; //length of image
  short palindex;
  short flags; //bit0 = 0 ldata; bit0 = 1 tdata
};
"""
class SFFPalNodeHeader(ctypes.Structure):
    _fields_ = [
            ('groupno', ctypes.c_short),
            ('itemno', ctypes.c_short),
            ('w',  ctypes.c_short),
            ('h',  ctypes.c_short),
            ('x',  ctypes.c_short),
            ('y',  ctypes.c_short),
            ('linked',  ctypes.c_short),
            ('fmt',  ctypes.c_uint8), #0=raw, 1=invalid, 2=RLE8, 3=RLE5, 4=LZ5
            ('colordepth',  ctypes.c_uint8), 
            ('offset', ctypes.c_long),
            ('len', ctypes.c_long)
            ('palindex',  ctypes.c_short),
            ('flags',  ctypes.c_short),
    ]


"""

struct _SFFV2_PAL_NODE_HEADER {
  short groupno;
  short itemno;
  short numcols;
  short linked;
  long offset; //offset into ldata
  long len; //len=0 => palette linked
};

"""
class SFFPalNodeHeader(ctypes.Structure):
    _fields_ = [
            ('groupno', ctypes.c_short),
            ('itemno', ctypes.c_short),
            ('numcols', ctypes.c_short),
            ('linked', ctypes.c_short),
            ('offset', ctypes.c_long),
            ('len', ctypes.c_long)
    ]