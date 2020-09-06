try:
    from . import context
    from .test_act import plot_palette
except:
    from test_act import  plot_palette
    import context 

from pymugen.formats.sff import SFF 
from pymugen.formats.images.sffv1 import from_file 
from pymugen.formats import act
import matplotlib.pyplot as plt

def plot_sprite(s):
    plt.subplot(211)
    print(s.image.max(),s.image.min(),s.image.mean())
    plt.imshow(s.image, cmap='gray')
    plt.subplot(212)
    plot_palette(s.palette)

def test_sffv1_read_1():
    #SFF V1
    sprites, h = from_file("G6_Luffy/Luffy.sff")
    s = sprites[3]
    plot_sprite(s)
    plt.show()
    print(h, s)

    sprites, h = from_file("android16/android16.sff")
    s = sprites[5]
    plot_sprite(s)
    plt.show()
    print(h, s)

def test_sff_wrapper_apply_palette():  
    #General
    sff = SFF("tests/test_data/android16/android16.sff")
    pal = act.from_file("tests/test_data/android16/arcade.act")
    img = sff.get_sprite(9000,1, pal)
    plt.subplot(121)
    plt.imshow(img, cmap='gray')
    plt.subplot(122)
    plot_palette(pal)
    plt.show()


def test_get_image():  
    #General
    sff = SFF("tests/test_data/android16/android16.sff")
    img = sff.get_image(9000,1)
    plt.imshow(img)
    plt.show()

if __name__ == "__main__":
    #test_sff_wrapper_apply_palette()
    test_get_image()