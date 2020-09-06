from . import context
from pymugen.formats.snd import Snd

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