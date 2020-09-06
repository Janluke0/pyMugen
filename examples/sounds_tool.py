
import context
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib

import numpy as np
import tkinter as tk
from tkinter import ttk

import wave 
import pyaudio 

from pymugen.formats.snd import Snd

class SoundToolToolbar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)
        self.event_fire = parent.event
        self.snd_btn = tk.Button(self, text="Load sounds..", command=self._open_sounds)
        self.snd_btn.pack(side=tk.LEFT)

        
        self.play_btn = tk.Button(self, text="Play", command=lambda: self.event_fire("play_sound", None))
        self.play_btn.pack(side=tk.LEFT)
        
        self.extract_btn = tk.Button(self, text="Extract..", command=self._save_sound)
        self.extract_btn.pack(side=tk.LEFT)

        self.scale_sound = ttk.Scale(self, from_=0, command=self.sound_selected)
        self.scale_sound.pack(side=tk.RIGHT)
        self._img_i = tk.StringVar()
        tk.Label(self, textvariable=self._img_i).pack(side=tk.RIGHT)


        self.combo_group = ttk.Combobox(master=self, values=[])
        self.combo_group.bind("<<ComboboxSelected>>", self.group_selected)
        self.combo_group.pack(side=tk.RIGHT)
        
        tk.Label(self, text="Group:").pack(side=tk.RIGHT)
    
    def _save_sound(self):
        fname = tk.filedialog.asksaveasfilename(
                    title = "Select where save the sound",
                    filetypes = (("WAV files","*.wav"),)
                )
        if fname != "":
            self.event_fire("save_sound", fname)

    def _open_sounds(self):
        fname = tk.filedialog.askopenfilename(
                    title = "Select sounds file",
                    filetypes = (("Sounds file","*.snd"),)
                )
        if fname != "":
            self.event_fire("new_sound", fname)

    def group_selected(self, evt):
        self.event_fire("group_select", self.combo_group.get())

    def sound_selected(self, val):
        val = int(float(val))
        self._img_i.set(str(val))
        self.event_fire("sound_select", val)


class SoundToolPlot(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)
        self.event_fire = parent.event
        self.fig = Figure(figsize=(5, 4), dpi=100)
        splot = self.fig.add_subplot(111)
        splot.axis('off')
        splot.text(0.5, 0.8, 'Sounds tool \n\n PyMUGEN', 
                    horizontalalignment='center', 
                    verticalalignment='center', 
                    wrap=True,
                    fontdict={'size': 24}
                )
        self.fig.canvas.draw()   

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

    def sound(self, samples):        
        self.fig.clf()
        splot = self.fig.add_subplot(111)
        splot.axis('off')
        splot.plot(samples)
        self.fig.canvas.draw()   

class SoundTool(tk.Frame):
    _snd = None
    _group = 0
    _sound = 0
    _ignore_next_evt = False #Hack

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)
        self.toolbar = SoundToolToolbar(self)
        self.toolbar.pack(side=tk.TOP, fill=tk.X, expand=True)

        self.plot = SoundToolPlot(self)
        self.plot.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)   

        self.master.wm_title("PyMUGEN: Sounds tool")

    def event(self, evt, arg):
        if not self._ignore_next_evt:
            if evt == "new_sound":
                self._snd = Snd(arg)
                self._group = next(iter(self._snd.groups.keys()))
                self._sound = self._snd.groups[self._group][0]
                self.master.wm_title(f"PyMUGEN: Sounds viewer - {arg}")
            elif evt == "group_select":
                self._group = int(arg)
                self._sound = self._snd.groups[self._group][0]
            elif evt == "sound_select":
                self._sound = arg
            elif evt == "save_sound":
                self._save_sound(arg)
            elif evt == "play_sound":
                self._play_sound()
            else:
                raise ValueError(f"Unvalid event:{evt}")
        
            self._update()
        else:
            self._ignore_next_evt = False

    def _update(self):
        d = {k:v for k,v in self._snd.groups.items()}

        self.toolbar.combo_group['values'] = (*d.keys(),)
        self.toolbar.combo_group.set(self._group)

        self.toolbar.scale_sound.configure(
                                from_= min(d[self._group]), 
                                to = max(d[self._group])
                            )
        self._ignore_next_evt = True
        self.toolbar.scale_sound.set(self._sound)
        s = self._snd.get_sound(self._group, self._sound)
        if s is not None:
            s = np.frombuffer(s[1], np.uint16)
            self.plot.sound(s)

    def _save_sound(self, fname):
        params, data = self._snd.get_sound(self._group, self._sound)
        dst = wave.open(fname, "w")
        dst.setparams(params)
        dst.writeframes(data)
        dst.close()

    def _play_sound(self):        
        params, data = self._snd.get_sound(self._group, self._sound)
        p = pyaudio.PyAudio()  
        #open stream  
        stream = p.open(format = p.get_format_from_width(params.sampwidth),  
                        channels = params.nchannels,  
                        rate = params.framerate,  
                        output = True)  

        stream.write(data)  
        stream.stop_stream()  
        stream.close()  
        p.terminate()  



if __name__ == "__main__":
    root = tk.Tk()
    SoundTool(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

