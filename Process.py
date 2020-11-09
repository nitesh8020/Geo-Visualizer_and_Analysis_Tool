import tkinter as tk
from tkinter import ttk
import rasterio
import earthpy.plot as ep
from rasterio.merge import merge
from rasterio.plot import show
import matplotlib
import numpy as np
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class Process(ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.master = master
        self.files=[]
        self.btns=[]
        self.display=ttk.Frame(self)
        self.createWidgets()


    def create(self):
        if self.display.winfo_exists():
            self.display.grid_forget()
            self.display.destroy()
            
        self.display = ttk.Frame(self)
        self.display.grid(row = 0, column = 1,rowspan=2, sticky = 'nwes')
        frame=self.display
        ff=[]
        for ffile in self.files:
            ff.append(rasterio.open(ffile))
        mos, out = merge(ff, method = self.dropdown.get())
        self.figure = Figure(figsize = (10,6), dpi = 100)
        self.plot = self.figure.add_subplot(1,1,1)
        # show(mos, cmap='terrain' , ax = self.plot)
        ep.plot_rgb((mos), stretch=True, str_clip = 0.5 , ax = self.plot)
        self.canvas = FigureCanvasTkAgg(self.figure,frame)
        self.toolbar = NavigationToolbar2Tk(self.canvas,frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack()

    def createWidgets(self):
        self.grid_columnconfigure(0,weight = 0)
        self.grid_columnconfigure(1,weight = 1)
        
        self.grid_rowconfigure(0,weight = 0)
        self.grid_rowconfigure(1,weight = 1)
        
        
        
        self.panel = ttk.Frame(self)
        self.panel.grid(row=1, column=0, sticky='nsew')
        
        self.txt = ttk.Label(self, text="Mosaic", font="Arial 15 bold")
        self.txt.grid(row=0, column=0,sticky='wens', padx=10, pady=10)
        
        
        self.btn = ttk.Button(self.panel, text='Choose scene...', command=self.choose)
        self.btn.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        
        self.createbtn = tk.Button(self, text='CREATE MOSAIC',bg='green', fg='white', command=self.create, state='disabled')
        self.createbtn.grid(row=4, column=0, sticky='nsew', padx=10, pady=10)
        
        self.lbl = ttk.Label(self.panel, text="Choose Mosaic Options", font="Arial 10")
        self.lbl.grid(row=2, column=0,sticky='wens', padx=10, pady=2)
        
        self.dropdown = ttk.Combobox(self.panel, values=['first','last','min', 'max'], state='readonly')
        self.dropdown.grid(row=3, column=0, sticky='nsew', padx=10, pady=10)
        self.dropdown.current(0)
        
        
    def choose(self, event=None):            # event handler for choose file
        ffile = filedialog.askopenfilename()
        if(ffile!=() and ffile!=''):
            ind= ffile.rfind('/')
            btn = ttk.Button(self.panel, text = ffile[ind+1:])
            btn.grid(row=len(self.btns)+4,column=0, sticky='nsew', padx=10, pady=10 )
            self.btns.append(btn)
            self.files.append(ffile)
            if(len(self.files)>=1):
                self.createbtn['state']='normal'
            
        

