from . import context
from pymugen.formats.images.pcx import read_file
import matplotlib.pyplot as plt

if __name__ == "__main__":
    #real colors - no palette
    img, pal = read_file("tests/test_data/drawhouse.pcx")
    print(pal)
    plt.imshow(img)
    plt.show()