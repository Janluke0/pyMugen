try:
    from . import context
except:
    import context 

from pymugen.formats._def import *

if __name__ == "__main__":
    r = from_file("tests/test_data/android16/android16.def")