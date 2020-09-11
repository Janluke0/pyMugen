try:
    from . import context
except:
    import context 
from pymugen.formats.fnt import from_file
from pymugen.formats.sff import apply_palette
import matplotlib.pyplot as plt

if __name__ == "__main__":
    font = from_file("tests/test_data/fonts/num1.fnt")
    print(font._conf)
    plt.imshow(apply_palette(*font._pcx))
    plt.show()
    font = from_file("tests/test_data/fonts/f-6x9.fnt")
    print(font._conf)
    plt.imshow(apply_palette(*font._pcx)[:,292:292+5])
    plt.show()