import sys
#sys.path.append("..")
from .utils.parser import parse
from ..entities.animations import *

#print(parse('kfm/kfm.air'))

#.air files can't work with configparser -> line by line
import os
def from_file(fname, encoding):
    with open(fname,"r", encoding=encoding) as fp:
        return from_stream(fp)

def from_stream(fp):
    actions = []
    action = None
    el = None
    clsn2, clsn1, clsn2_def, clsn1_def = [], [], [], []
    for l in fp.readlines():
        l = l.strip()
        if l.startswith(";") or l == "":
            continue
        l = l.split(";")[0]
        #ends previous action begin the new
        if l.startswith("[Begin Action"):
            if action is not None:
                #print("end", action)
                actions.append(action)
                clsn2.clear(), clsn1.clear()
                clsn2_def.clear(), clsn1_def.clear()
            # [Begin Action {code}]
            code = int(l.split("Action")[1].split("]")[0].strip())
            action = Action(code)
            #print("begin", action)
            pass

        #boxes 
        elif l.startswith("Clsn"):
            #header of boxes
            if ":" in l:
                tmp = l.replace("Clsn", "")
                boxes_type, boxes_count = tmp.split(":")
                if "Default" in boxes_type:
                    pass #TODO: what to do?
                else:
                    if "2" in boxes_type:
                        clsn2.clear()
                    elif "1" in boxes_type:
                        clsn1.clear()

            #box values
            else:
                _type, values = l.split("=")
                box = Box(*[int(v) for v in values.split(",") if v.strip() !=""])
                if "2Def" in _type:
                    clsn2_def.append(box)
                if "1Def" in _type:
                    clsn1_def.append(box)
                elif "2" in _type:
                    clsn2.append(box)
                elif "1" in _type:
                    clsn1.append(box)
                else:
                    print("unkwon type", _type)

        #animation elements
        elif 'loop' in l.lower():
            action.animation_elements.append(LOOP_START)

        #animation elements
        else:
            c_boxes = clsn2_def.copy()
            c_boxes.extend(clsn2)

            a_boxes = clsn1_def.copy()
            a_boxes.extend(clsn1)
            values = [v.strip() for v in l.split(",") if v != ""]
            el = AnimationElement(c_boxes, a_boxes
                                , int(values[0]) #group_number
                                , int(values[1]) #image_number
                                , int(values[2]) #x_offset
                                , int(values[3]) #y_offset
                                , int(values[4]) #time
                                , values[5:] if len(values)>5 else None) #effects
            action.animation_elements.append(el)
    return actions


def parse_air(fname, encoding='utf-8-sig'):
    return from_file(fname,encoding)
