try:
    from . import context
except:
    import context 
from pymugen.formats import Act
import numpy as np

import unittest as ut
import os 

def plot_palette(palette):
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    tmp = np.array([n for n in range(256)]).reshape(16,16)
    plt.imshow(tmp,cmap=ListedColormap(palette/255))
    plt.show()

if __name__ == "__main__":
    with Act("tests/test_data/G6_Luffy/1.act") as act:
        plot_palette(act._data)

class ActReading(ut.TestCase):
    fname_test = "tests/test_data/test.save.act"
    def _tearDown(self):
        if os.path.isfile(self.fname_test):
            os.remove(self.fname_test)
        return super().tearDown()

    def test_open(self):
        fname = "tests/test_data/G6_Luffy/{0}.act"
        for n in range(1,7):            
            with Act(fname.format(n)) as act:
                self.assertIsNotNone(act)
    #@ut.skip    
    def test_save(self):
        fname = "tests/test_data/G6_Luffy/1.act"
        act = Act(fname)
        act.save(self.fname_test)
        
        act2 = Act(self.fname_test)
        self.assertEqual(act,act2)
        act2.close(), act.close() 
    
    def test_change_color(self):
        with Act(self.fname_test) as act:
            act[0] = 42, 42, 42
            self.assertTupleEqual(act[0], (42, 42, 42))
            act.save()
        
        with Act(self.fname_test) as act:
            self.assertTupleEqual(act[0], (42, 42, 42))

    def test_new_file(self):
        if os.path.isfile(self.fname_test):
            os.remove(self.fname_test)

        with Act(self.fname_test) as act:
            act[:] = ((42, 42, 42),)*256
            act.save()

        with Act(self.fname_test) as act:
            self.assertTupleEqual(act[0], (42, 42, 42))
            self.assertTupleEqual(act[42], (42, 42, 42))