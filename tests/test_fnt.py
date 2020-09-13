try:
    from . import context
except:
    import context 
from pymugen.formats.fnt import from_file
from pymugen.formats.sff import apply_palette
import matplotlib.pyplot as plt
from pymugen.formats import Fnt
import unittest as ut
import os
import numpy as np

def plot_text(font_img, shape, _map,text):
    out = np.zeros((shape[1], shape[0]*len(text) + len(text), 3))
    print(out.shape, font_img.shape)
    for i,c in enumerate(text):
        print(c)
        ci = _map[c]
        char = font_img[:,ci[0]:ci[0]+ci[1]]
        if char.shape[1] < 5:
            t = np.zeros((char.shape[0],5,3))
            t[:,:char.shape[1]] = char
            char = t
        out[:,i*5:(i+1)*5] = char
    plt.imshow(out)
    plt.show()

if __name__ == "__main__":
    font = from_file("tests/test_data/fonts/f-6x9.fnt")
    print(font._conf)
    plot_text(apply_palette(*font._pcx), font._conf['def']['size'], font._conf['map'], "CIAOCiAo!?")
    exit()
    
    font = from_file("tests/test_data/fonts/num1.fnt")
    print(font._conf)
    plt.imshow(apply_palette(*font._pcx))
    plt.show()


class FntTest(ut.TestCase):
    def test_open(self):
        with Fnt("tests/test_data/fonts/num1.fnt") as fnt:
            self.assertIsNotNone(fnt)
            self.assertIsNotNone(fnt['0'])
            for char, img in fnt:
                self.assertTrue(type(char) is str and len(char)==1)
            self.assertTrue(True)
            
    @ut.skip
    def test_save(self):
        dst = "/tests/test_data/test.save.fnt"
        with Fnt("tests/test_data/fonts/num1.fnt") as fnt:
            fnt.save(dst)
            self.assertTrue(os.path.isfile(dst))