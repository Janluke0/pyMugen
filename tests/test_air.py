try:
    from . import context
except:
    import context 
from pymugen.formats.air import parse_air
import matplotlib.pyplot as plt


if __name__ == "__main__":
    actions = parse_air('tests/test_data/kfm/kfm.air')
    #the first action which contains at least an attack boxes
    a = next((i for i,a in enumerate(actions) 
                if len([el for el in a.animation_elements 
                        if type(el) != str and len(el.attack_boxes) > 0
                    ]) > 0 
        ))
    #a = 1
    for el in actions[a].animation_elements:
        print(actions[a].code, el)