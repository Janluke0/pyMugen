import context
from frames import MatplotlibFrame

import matplotlib
import threading
import logging
import numpy as np
import tkinter as tk
from tkinter import ttk

from pymugen.formats.sff import SFF
from pymugen.formats import act, air#.from_file

log = logging.getLogger("Animations tool")

class SpriteToolToolbar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)
        self.event_fire = parent.event
        self.spr_btn = tk.Button(self, text="Load sprites..", command=self._open_sprites)
        self.spr_btn.pack(side=tk.LEFT)

        self.pal_btn = tk.Button(self, text="Load palette..", command=self._open_palette)
        self.pal_btn.pack(side=tk.LEFT)
        
        self.air_btn = tk.Button(self, text="Load air..", command=self._open_air)
        self.air_btn.pack(side=tk.LEFT)

        self.check_def = tk.Checkbutton(self, text="LOOP", command=self._force_loop)
        self.check_def.pack(side=tk.LEFT)
        
        self.extract_btn = tk.Button(self, text="Extract..", command=self._save_image)
        self.extract_btn.pack(side=tk.LEFT)

        self.combo_anim = ttk.Combobox(master=self, values=[])
        self.combo_anim.bind("<<ComboboxSelected>>", self.anim_selected)
        self.combo_anim.pack(side=tk.RIGHT)
        
        tk.Label(self, text="Animation:").pack(side=tk.RIGHT)
    
    def _save_image(self):
        fname = tk.filedialog.asksaveasfilename(
                    title = "Select where save the image",
                    filetypes = (("Image files","*.gif"),)
                )
        if fname != "":
            self.event_fire("save_anim", fname)

    def _open_sprites(self):
        fname = tk.filedialog.askopenfilename(
                    title = "Select sprites file",
                    filetypes = (("Sprites file","*.sff"),)
                )
        if fname != "":
            self.event_fire("new_sprites", fname)

    def _open_palette(self):
        fname = tk.filedialog.askopenfilename(
                    title = "Select palette file",
                    filetypes = (("palette file","*.act"),)
                )
        if fname != "":
            self.event_fire("new_palette", fname)
    
    def _open_air(self):
        fname = tk.filedialog.askopenfilename(
                    title = "Select air file",
                    filetypes = (("Animation file","*.air"),)
                )
        if fname != "":
            self.event_fire("new_air", fname)

    def anim_selected(self, evt):
        self.event_fire("anim_select", self.combo_anim.get())

    def _force_loop(self):
        self.event_fire("force_loop", None)


class AnimationTool(tk.Frame):
    _pal = None
    _sff = None
    _air = None
    _anim_th = None
    _img = None
    _anim = 0
    _use_def_pal = False
    _ignore_next_evt = False #Hack
    _force_loop = False

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)

        self.toolbar = SpriteToolToolbar(self)
        self.toolbar.pack(side=tk.TOP, fill=tk.X, expand=True)

        
        self.progress_bar = ttk.Progressbar(self)
        self.progress_bar.pack(side=tk.BOTTOM, fill=tk.X, expand=True) 

        self.plot = MatplotlibFrame(self, banner='Animations tool \n\n PyMUGEN')
        self.plot.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)  

        self.master.wm_title("PyMUGEN: Animations tool")

        self.master.after(100,self._update)

    def event(self, evt, arg):
        if not self._ignore_next_evt:
            if evt == "new_sprites":
                th = threading.Thread(target=self._load_sff,args=(arg,)) 
                th.start()
                self._group = 0
                self._image = 0
               # self.master.wm_title(f"PyMUGEN: Animations tool - {arg}")
            elif evt == "new_palette":
                self._pal = act.from_file(arg)
            elif evt == "new_air":
                self._air = air.parse_air(arg,'latin-1')
            elif evt == "anim_select":
                self._anim = int(arg)
                if self._anim_th is not None and self._anim_th.is_alive():
                    self._anim_th.join()
                self._anim_th = threading.Thread(target=self._do_anim) 
                self._anim_th.start()
            elif evt == "force_loop":
                self._force_loop = not self._force_loop
            elif evt == "save_anim":
                self._save_anim(arg)
            else:
                raise ValueError(f"Unvalid event:{evt}")
                
        else:
            self._ignore_next_evt = False

    def _update(self):
        if self._sff is not None and self._air is not None:
            self.toolbar.combo_anim['values'] = [a.code for a in self._air]
            self.toolbar.combo_anim.set(self._anim)
            if self._img is not None:
                self.plot.image(self._img)
        self.master.after(500,self._update)

    def _do_anim(self):
        import time
        anim = next((a for a in self._air if a.code == self._anim))
        #60 tick ps 
        not_stop = True
        while not_stop:
            for el in anim.animation_elements:
                if el == air.LOOP_START:
                    print("LOOP START")
                    break
                #print("update img")
                self._img = self._sff.get_image(
                            el.group_number,el.image_number,
                            self._pal
                        )
                if el.time < 0: break
                if anim.code != self._anim: break
                time.sleep(el.time/60)
            if anim.code != self._anim: break
            not_stop = self._force_loop
            

    def _save_anim(self, fname):
        from PIL import Image
        anim = next((a for a in self._air if a.code == self._anim))
        #60 tick ps = 1/60 s = 1000/60 ms ~= 16ms per frame
        max_w, max_h = 0, 0
        frames = []
        for el in anim.animation_elements:
            if el == air.LOOP_START:
                print("LOOP START")
                #TODO:handle animation loop correctly
                continue
            frame = self._sff.get_image(
                            el.group_number,el.image_number
                            ,self._pal, _type="cmap"
                        )
            p = self._pal if self._pal is not None else self._sff.tmp[el.group_number][el.image_number].palette.data
            frame = Image.fromarray(frame).convert('P') 
            if frame.size[0] > max_w: max_w = frame.size[0]
            if frame.size[1] > max_h: max_h = frame.size[1]
            frames.extend([frame]*abs(el.time))
        from PIL import ImagePalette
        p = ImagePalette.ImagePalette(mode='RGB', palette=bytearray(p.reshape(-1, order='F')))
        base = Image.new("RGB",(max_w, max_h)).convert('P') 
        base.save(fname, save_all=True
                    , duration=16, append_images=frames
                    , loop=0, trasparency=0,palette=p)

    def _load_sff(self, fname):
        def prog(actual, total):
            self.progress_bar.step(100/total) 
        self._sff  = SFF(fname, prog)
        

if __name__ == "__main__":
    root = tk.Tk()
    AnimationTool(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
