from . import context
from pymugen.formats.fnt import from_file
import matplotlib.pyplot as plt

if __name__ == "__main__":
    font = from_file("tests/test_data/fonts/num1.fnt")
    print(font._text)
    plt.imshow(font._pcx[0])
    plt.show()
    font = from_file("tests/test_data/fonts/f-6x9.fnt")
    print(font._text)
    plt.imshow(font._pcx[0])
    plt.show()