# PyMUGEN

This project aim to be a module to read all the formats used by the mugen 
and in a second time, a compatible reimplementation of that lovely piece of software.



## What is working?

Some buggy examples are avaible

### sff(v1) and act formats

    from pymugen.formats.sff import SFF 
    import matplotlib.pyplot as plt

    sff = SFF("Tizio/Tizio.sff")
    pal = act.from_file("Tizio/pal1.act")
    # the sprite 0 in the group 1 
    img = sff.get_sprite(1,0, pal)
    plt.imshow(img)
    plt.show()

### snd format

    from pymugen.formats.snd import Snd
    import matplotlib.pyplot as plt

    snd = Snd("Tizio/Tizio.snd")
    # the sound 1 in the group 0 
    params, data = snd.get_sound(0,1)
    dst = wave.open("file.wav", "w")
    dst.setparams(params)
    dst.writeframes(data)
    dst.close()

### cns format

    from pymugen.formats.cns import parse_cns
    states, orphan_ctrls = parse_cns("Tizio/Tizio.cns", 'latin-1')

### fnt format

image is extracted correctly but more work is required