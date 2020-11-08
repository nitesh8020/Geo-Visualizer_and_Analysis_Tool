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
#from clipmosaic.py import clipping

class Process(ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.master = master
        self.files=[]
        self.btns=[]
        self.cfile=''
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
        
        self.shbtn = tk.Button(self, text='select Shapefile', command=self.shapefile)
        self.shbtn.grid(row=5, column=0, sticky='nsew', padx=10, pady=10)
        
        self.cpbtn = tk.Button(self, text='clip mosaic', command=self.ClipImage)
        self.cpbtn.grid(row=6, column=0, sticky='nsew', padx=10, pady=10)
        
    def shapefile(self, event=None):
        self.cfile = filedialog.askopenfilename()
        if(self.cfile!=() and self.cfile!=''):
            ind= self.cfile.rfind('/')
            self.shbtn["text"]='shape: '+self.file2[ind+1:]
        else: self.cfile=''
                
    def ClipImage(self, event=None):
        if self.window.winfo_exists():
            self.window.grid_forget()
            self.window.destroy()
        self.header['text'] = 'Clip the Mosaic'
        self.window = Clipping(self)
        self.window.grid(row=1, column=0, columnspan=4, sticky='nsew')
        
    def choose(self, event=None):			# event handler for choose file
        ffile = filedialog.askopenfilename()
        if(ffile!=() and ffile!=''):
            ind= ffile.rfind('/')
            btn = ttk.Button(self.panel, text = ffile[ind+1:])
            btn.grid(row=len(self.btns)+4,column=0, sticky='nsew', padx=10, pady=10 )
            self.btns.append(btn)
            self.files.append(ffile)
            if(len(self.files)>=1):
                self.createbtn['state']='normal'
            
        

