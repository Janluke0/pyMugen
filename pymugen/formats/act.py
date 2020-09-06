
import struct 
import numpy as np

def from_file(fname):
    data = []
    with open(fname, "rb") as actFile:
        for _ in range(256):
            raw = actFile.read(3)
            color = struct.unpack("3B", raw)
            data.append(color)
    data.reverse()
    return np.asarray(data)

