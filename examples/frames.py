
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
class MatplotlibFrame(tk.Frame):
    def __init__(self, parent, banner=None, *args, **kwargs):
        tk.Frame.__init__(self, parent)
        self.event_fire = parent.event
        self.fig = Figure(figsize=(5, 4), dpi=100)
        if banner is not None:
            splot = self.fig.add_subplot(111)
            splot.axis('off')
            splot.text(0.5, 0.8, banner, 
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
    
    def image(self, img):        
        self.fig.clf()
        splot = self.fig.add_subplot(111)
        splot.axis('off')
        splot.imshow(img, cmap="gray")
        self.fig.canvas.draw()   