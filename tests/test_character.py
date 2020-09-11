try:
    from . import context
except:
    import context 
from pymugen.entities.character import *
import os
if __name__=='__main__':
    c = Character('./tests/test_data/android16','android16')

    print(c._snd.groups)
    print(c._sff.groups)
    print(c._air)
    print(c._palettes)
    
