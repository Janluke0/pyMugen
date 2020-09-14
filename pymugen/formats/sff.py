from .images import sffv1
from collections import namedtuple
import numpy as np
#import  sffv2 

#NOTE:https://mugenguild.com/forum/topics/sffv2-format-information-106218.0.html
#https://github.com/naclander/openmugen/blob/7a3964735516d96c59e84ce242b070184b4f306a/structs.h
class SFFSprite:
    __transparency_color_index = 0
    def __init__(self, header, palettes):
        super().__init__()
        self.header = header
        self.palettes = palettes
        self.group_n = header.groupno
        self.image_n = header.imageno

    @property
    def palette(self):
        return self.palettes[self.header.linked]        
        
    def as_image(self, _type="rgba", palette=None, use_PIL=False):
        """
            type: str [rgba,   rgb   or cmap]
                      (x,y,4), (x,y,3), (x,y)
            --------
            Returns:
                np.ndarray[int]
        """
        h = self.header
        if palette is None:
            img = SFFSprite._apply_palette(h.image, self.palette.data, _type, use_PIL)
        elif isinstance(palette,int):
            img = SFFSprite._apply_palette(h.image, self.palettes[palette].data, _type, use_PIL)
        else:
            img = SFFSprite._apply_palette(h.image, palette, _type, use_PIL)
            
        return img

    @staticmethod
    def _apply_palette(img, pal, _type, use_pil):
        if use_pil:
            from PIL import Image

        if _type == "rgb":
            out = np.empty((*img.shape,3), dtype=np.uint8)
            for i in range(out.shape[0]):
                for j in range(out.shape[1]):
                    out[i,j,:] = pal[img[i,j]]
        elif _type == "rgba":
            out = np.empty((*img.shape,4), dtype=np.uint8)
            for i in range(out.shape[0]):
                for j in range(out.shape[1]):
                    t = img[i,j]
                    out[i,j,0] = pal[t,0]
                    out[i,j,1] = pal[t,1]
                    out[i,j,2] = pal[t,2]
                    if t == SFFSprite.__transparency_color_index:
                        out[i,j,3] = 0
                    else:
                        out[i,j,3] = 255
        elif _type == "cmap":
            if use_pil:
                return Image.fromarray(img)
            else:
                return img
            
        
        if use_pil:
            return Image.fromarray(out)
        else:
            return out

SFFPalette = namedtuple("SFFPalette",["group","n","data"])

class SFF:
    def __init__(self, file, progress_cb=None):
        super().__init__() 
            #TODO: check format       
        if True:# is V1
            t = sffv1.from_file(file,progress_cb)
            self._sprites, self._header, self._palettes = (*t,)
            self.tmp = {}
            for s in self._sprites:
                spr = SFFSprite(s, self._palettes)
                if s.groupno not in self.tmp:
                    self.tmp[s.groupno] = {s.imageno:spr}
                else:                        
                    self.tmp[s.groupno][s.imageno] = spr
        else:# is V2
            pass

    def get_image(self, groupno, imageno, palette=None, _type="rgba", use_PIL=False):
        spr = self.tmp[groupno][imageno]
        return spr.as_image(palette=palette, _type=_type, use_PIL=use_PIL)
        
    #TODO return SFFSprite
    def get_sprite(self, groupno, imageno, palette=None, ret_alphas=False):
        img = None
        _s = None
        for s in self._sprites:
            if s.imageno==imageno and s.groupno == groupno:
                _s = s
                if palette is None:
                    img = s.image
                elif isinstance(palette,str) and palette == "default":
                    if s.linked != 0:
                        p = self.palettes[s.linked].data
                    else:
                        p = s.palette
                    img = apply_palette(s.image, p)
                elif isinstance(palette,int):
                    img = apply_palette(s.image, self._palettes[palette].data)
                else:
                    img = apply_palette(s.image, palette)
                break

        if ret_alphas:
            alphas = np.ones(_s.image.shape)
            for i in range(alphas.shape[0]):
                for j in range(alphas.shape[1]):
                    alphas[i,j] = _s.image[i,j] != 0 
            return img, alphas
        return img

    @property
    def groups(self):
        group_nums = {s.groupno for s in self._sprites}
        groups = {}
        for gn in group_nums:
            groups[gn] = [s.imageno for s in self._sprites if s.groupno == gn]
        return groups

def apply_palette(img, pal):
    out = np.empty((*img.shape,3), dtype=np.uint8)
    for i in range(out.shape[0]):
        for j in range(out.shape[1]):
            out[i,j,:] = pal[img[i,j]]
    return out