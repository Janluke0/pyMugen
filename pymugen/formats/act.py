
import struct 
import numpy as np
from ._base import AbstractFormat
from deprecated import deprecated

@deprecated
def from_file(fname):
    data = []
    with open(fname, "rb") as actFile:
        for _ in range(256):
            raw = actFile.read(3)
            color = struct.unpack("3B", raw)
            data.append(color)
    data.reverse()
    return np.asarray(data)

class Act(AbstractFormat):       
    _formats_avaible = ["act"]
    def __init__(self, source, *args, **kwargs):
        super().__init__(source, encoding=None, read_mode="rb", write_mode="wb", *args, **kwargs)
        if self._data is None:
            self._data = np.zeros((256,3), dtype="u8")

    def get_item(self, index):
        if type(index) == int and (index < 0 or index >255):
            raise IndexError()

        if type(index) == slice:
            start, stop, _ = index.indices(2)
            if start < 0 or stop >255:
                raise IndexError()

        return (*self._data[index],)

    def set_item(self, index, value=None):
        self._data[index] = np.array(value)
   
    def get_keys(self):
        return {k:(0,1,2) for k in range(256)}
   
    def _read(self):
        #print("READ")
        self._data = []
        for _ in range(256):
            raw = self._buff.read(3)
            #print(raw)
            color = struct.unpack("3B", raw)
            #print("read:",raw, color)
            self._data.append(color)
        self._data.reverse()
        self._data = np.asarray(self._data)

    def _write(self, _format):
        #print("WRITE")
        for i in range(255,-1,-1):
            raw = struct.pack("3B", *self._data[i])
            #print("write:",self._data[i],raw, struct.unpack("3B", raw))
            self._out_buff.write(raw)