try:
    from . import context
except:
    import context 
from pymugen.formats import Snd
import unittest as ut
import wave 

if __name__ == "__main__":
    snd = Snd("tests/test_data/G6_Luffy/Luffy.snd")
    #for s in sounds:
    #    print(s)
    snd = Snd("tests/test_data/kfm/kfm.snd")
    params, data = snd.get_sound(0,1)
    print(snd.groups, len(snd._sounds))
    dst = wave.open("tests/test_data/file.wav", "w")
    dst.setparams(params)
    dst.writeframes(data)
    dst.close()

class SndTest(ut.TestCase):
    def test_open(self):
        with Snd("tests/test_data/kfm/kfm.snd") as snd:
            self.assertIsNotNone(snd)
            self.assertIsNotNone(snd[0,0])
            for (group, n), wav in snd:
                pass
            self.assertTrue(True)