try:
    from . import context
except:
    import context 
from pymugen.formats.act import from_file
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

import unittest as ut

def plot_palette(palette):
    tmp = np.array([n for n in range(256)]).reshape(16,16)
    plt.imshow(tmp,cmap=ListedColormap(palette/255))

if __name__ == "__main__":
    p = from_file("tests/test_data/G6_Luffy/1.act")
    fname = "tests/test_data/G6_Luffy/{0}.act"
    fig = plt.figure()
    fig.canvas.set_window_title("Luffy palettes")
    for n in range(1,7):
        plt.subplot(3,2,n)
        palette = from_file(fname.format(n))
        plot_palette(palette)
    plt.show()

class ActReading(ut.TestCase):
    def test_open(self):
        fname = "tests/test_data/G6_Luffy/{0}.act"
        for n in range(1,7):
            palette = from_file(fname.format(n))
            self.assertIsNotNone(palette)