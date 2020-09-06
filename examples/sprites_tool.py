import context
from frames import MatplotlibFrame

import matplotlib
import threading
import logging
import numpy as np
import tkinter as tk
from tkinter import ttk

from pymugen.formats.sff import SFF
from pymugen.formats import act #.from_file

log = logging.getLogger("Sprites tool")

class SpriteToolToolbar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)
        self.event_fire = parent.event
        self.spr_btn = tk.Button(self, text="Load sprites..", command=self._open_sprites)
        self.spr_btn.pack(side=tk.LEFT)

        self.pal_btn = tk.Button(self, text="Load palette..", command=self._open_palette)
        self.pal_btn.pack(side=tk.LEFT)

        self.check_def = tk.Checkbutton(self, text="use default palette", command=self._use_def)
        self.check_def.pack(side=tk.LEFT)
        
        self.extract_btn = tk.Button(self, text="Extract..", command=self._save_image)
        self.extract_btn.pack(side=tk.LEFT)

        self.scale_image = ttk.Scale(self, from_=0, command=self.image_selected)
        self.scale_image.pack(side=tk.RIGHT)
        self._img_i = tk.StringVar()
        tk.Label(self, textvariable=self._img_i).pack(side=tk.RIGHT)


        self.combo_group = ttk.Combobox(master=self, values=[])
        self.combo_group.bind("<<ComboboxSelected>>", self.group_selected)
        self.combo_group.pack(side=tk.RIGHT)
        
        tk.Label(self, text="Group:").pack(side=tk.RIGHT)
    
    def _save_image(self):
        fname = tk.filedialog.asksaveasfilename(
                    title = "Select where save the image",
                    filetypes = (("PNG files","*.png"),)
                )
        if fname != "":
            self.event_fire("save_image", fname)

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
    
    def group_selected(self, evt):
        self.event_fire("group_select", self.combo_group.get())

    def image_selected(self, val):
        val = int(float(val))
        self._img_i.set(str(val))
        self.event_fire("image_select", val)

    def _use_def(self):
        self.event_fire("use_def", None)


class SpriteTool(tk.Frame):
    _pal = None
    _sff = None
    _group = 0
    _image = 0
    _use_def_pal = False
    _ignore_next_evt = False #Hack

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)

        self.toolbar = SpriteToolToolbar(self)
        self.toolbar.pack(side=tk.TOP, fill=tk.X, expand=True)

        
        self.progress_bar = ttk.Progressbar(self)
        self.progress_bar.pack(side=tk.BOTTOM, fill=tk.X, expand=True) 

        self.plot = MatplotlibFrame(self, banner='Sprites tool \n\n PyMUGEN')
        self.plot.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)  

        self.master.wm_title("PyMUGEN: Sprites tool")

        self.master.after(500,self._update)

    def event(self, evt, arg):
        if not self._ignore_next_evt:
            if evt == "new_sprites":
                th = threading.Thread(target=self._load_sff,args=(arg,)) 
                th.start()
                self._group = 0
                self._image = 0
                self.master.wm_title(f"PyMUGEN: Sprites tool - {arg}")
            elif evt == "new_palette":
                self._pal = act.from_file(arg)
            elif evt == "group_select":
                self._group = int(arg)
                self._image = 0
            elif evt == "image_select":
                self._image = arg
            elif evt == "use_def":
                self._use_def_pal = not self._use_def_pal
            elif evt == "save_image":
                self._save_image(arg)
            else:
                raise ValueError(f"Unvalid event:{evt}")
                
        else:
            self._ignore_next_evt = False

    def _update(self):
        if self._sff is not None:
            d = {k:v for k,v in self._sff.groups.items()}

            self.toolbar.combo_group['values'] = (*d.keys(),)
            self.toolbar.combo_group.set(self._group)

            self.toolbar.scale_image.configure(to = max(d[self._group]))
            self._ignore_next_evt = True
            self.toolbar.scale_image.set(self._image)
            try:
                self.plot.image(
                    self._sff.get_image(
                        self._group, self._image, 
                        self._pal if not self._use_def_pal else None
                    ))
            except Exception as e:
                log.exception(e)
                
        self.master.after(500,self._update)

    def _save_image(self, fname):
        img = self._sff.get_image(
                self._group, self._image, 
                self._pal if not self._use_def_pal else None)
        matplotlib.image.imsave(fname,img, cmap='gray')

    def _load_sff(self, fname):
        self._sff  = SFF(fname
                        , lambda _,tot:self.progress_bar.step(100/tot)
                    )
        

if __name__ == "__main__":
    root = tk.Tk()
    SpriteTool(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
