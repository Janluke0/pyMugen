import os
import io
from abc import ABC, abstractmethod, abstractproperty


class AbstractFormat(ABC):
    _read_mode = "r"
    _write_mode = "w"
    _encoding = "utf-8"
    _max_keys = 1
    _formats_avaible = []
    _data = None
    _buff = None
    _out_buff = None
    def __init__(self, file=None, encoding="utf-8",
                read_mode="r", write_mode="w", 
                *args, **kwargs):

        self._read_mode = read_mode
        self._write_mode = write_mode
        self._encoding = encoding

        self.source = file
        if self.source is not None:
            self.open(self.source)

    def close(self):
        if self._buff is not None and not self._buff.closed:
           self._buff.close()
           while not self._buff.closed: pass
        
        if self._out_buff is not None and not self._out_buff.closed:
           self._out_buff.close()
           while not self._out_buff.closed: pass


    @abstractmethod
    def get_item(self, *keys):
        pass
    
    @abstractmethod
    def set_item(self, *keys, value=None):
        pass
    
    @abstractmethod
    def get_keys(self):
        pass

    @abstractmethod
    def _read(self):
        """ parse the file from self._buff"""
        raise NotImplementedError()
    
    @abstractmethod
    def _write(self, _format):
        """ write the file to self._out_buff int the supplied format"""
        raise NotImplementedError()

    def save(self, file=None, _format=None):
        """
            file: file like object, path or none
                if None the readed file will be overwrite 
            format: str or none
                if not present in self._formats_avaible a exception will be raised
                if none it will be guess (if file is path) or the first will be used
        """
        if file is None:
            file = self.source
        if _format is None:
            if type(file) == str:
                f = file.split('.')[-1].lower()
                if f in self._formats_avaible:
                    _format = f 
                else:
                    _format = self._formats_avaible[0]
        if _format not in self._formats_avaible:
            raise ValueError("Unvalid format")
        
        if hasattr(file, 'write'):
            self._out_buff = file
            self._write(_format)

        if type(file) is str:
            self._out_buff = open(file, self._write_mode, encoding=self._encoding)
            self._write(_format)
            self._out_buff.close()

    def open(self,file, mode="read"):
        if isinstance(self.source, str):
            if os.path.exists(self.source) and mode != "write":
                self._buff = open(
                    self.source, self._read_mode, 
                    encoding=self._encoding
                    )
            else:
                self._out_buff = open(
                    self.source, self._write_mode, 
                    encoding=self._encoding
                    )
        else:
            self._buff = self.source
        if self._buff is not None:
            self._read()

    def _check_keys(self, keys):
        if hasattr(keys,"__iter__") and len(keys) > self._max_keys:
            raise KeyError("Unvaild key")

    def __iter__(self):
        for k in self.get_keys():
            if hasattr(k,"__iter__"):
                yield k, self.get_item(*k)
            else:
                yield k, self.get_item(k)

    def __setitem__(self, keys, value):
        #print(keys, value)
        self._check_keys(keys)
        if hasattr(keys,"__iter__"):
            return self.set_item(*keys,value=value)
        else:
            return self.set_item(keys,value=value)

    def __getitem__(self, keys):
        self._check_keys(keys)
        if hasattr(keys,"__iter__"):
            return self.get_item(*keys)
        else:
            return self.get_item(keys)

    def __contains__(self, keys):
        self._check_keys(keys)
        return keys in self.get_keys()

    def __eq__(self, value):
        return (
            self.__class__ == value.__class__ and
            self._data is not None and
            #TODO: in subclass
            (self._data == self._data).all()
        )
    
    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()

