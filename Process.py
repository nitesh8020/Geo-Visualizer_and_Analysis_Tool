import os
import glob
import tkinter as tk
from tkinter import ttk
import rasterio
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
from rasterio.merge import merge
from rasterio.plot import show
import matplotlib
import numpy as np
from tkinter import filedialog
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class Process(ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.master = master
        self.files=[]
        self.btns=[]
        self.histbtns=[]
        self.histfiles=[]
        self.display=ttk.Frame(self)
        self.createWidgets()


    def create(self):
        if self.display.winfo_exists():
            self.display.grid_forget()
            self.display.destroy()
            
        self.display = ttk.Frame(self)
        self.display.grid(row = 0, column = 4,rowspan=2, sticky = 'nwes')
        frame=self.display
        ff=[]
        for ffile in self.files:
            ff.append(rasterio.open(ffile))
        mos, out = merge(ff, method = self.dropdown.get())
        self.figure = Figure(figsize = (6,4), dpi = 100)
        self.plot = self.figure.add_subplot(1,1,1)
        # show(mos, cmap='terrain' , ax = self.plot)
        ep.plot_rgb((mos), stretch=True, str_clip = 0.5 , ax = self.plot)
        self.canvas = FigureCanvasTkAgg(self.figure,frame)
        self.toolbar = NavigationToolbar2Tk(self.canvas,frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack()

    def viewhist(self):
        if self.display.winfo_exists():
            self.display.grid_forget()
            self.display.destroy()
        
        self.display = ttk.Frame(self)
        self.display.grid(row = 0, column = 4,rowspan=2, sticky = 'nwes')
        frame=self.display

        band_path=[]
        for file in self.histfiles:
            band_path.append(file)
        
        # dir = self.dir[0]
        # band_path = glob.glob(os.path.join(dir,"*.tif"))
        # band_path = glob.glob(os.path.join(dir,"*.TIF"))
        band_path.sort()
        band_stack, meta_data = es.stack(band_path, nodata=-9999)
        size = len(band_path)
        color_list = ["Indigo","Blue","Green","Yellow","Red","Maroon","Purple","Violet"]
        titles = []
        for i in range(size):
            titles.append("File"+str(i+1))
        self.figure,self.plot = ep.hist(band_stack, title = titles,figsize = (6,4))
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

        self.histogramPanel = ttk.Frame(self)
        self.histogramPanel.grid(row = 1, column = 1, sticky = 'nsew')

        self.down = ttk.Frame(self)
        self.down.grid(row = 2, column = 0, sticky = 'sw', columnspan = 4)
        
        self.txt = ttk.Label(self.panel, text="Mosaic", font="Arial 15 bold")
        self.txt.grid(row=0, column=0,sticky='wens', padx=10, pady=10)
        
        self.text = ttk.Label(self.histogramPanel, text="Histogram", font="Arial 15 bold")
        self.text.grid(row=0, column=1, sticky="wens", padx=10, pady=10)
        
        self.dirbtn = ttk.Button(self.histogramPanel, text='Choose BandFile', command=self.choosehist)
        self.dirbtn.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)

        self.btn = ttk.Button(self.panel, text='Choose scene...', command=self.choose)
        self.btn.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        
        self.createbtn = tk.Button(self.down, text='CREATE MOSAIC',bg='green', fg='white', command=self.create, state='disabled')
        self.createbtn.grid(row=4, column=0, sticky='nsew', padx=10, pady=10, columnspan=1)

        self.histbtn = tk.Button(self.down, text='VIEW HISTOGRAM',bg='green', fg='white', command=self.viewhist, state='disabled')
        self.histbtn.grid(row=4, column=1, sticky='nsew', padx=10, pady=10, columnspan=1)
        
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

    def choosehist(self, event=None):            # event handler for choosing directory
        histfile = filedialog.askopenfilename()
        if(histfile!=() and histfile!=''):
            ind= histfile.rfind('/')
            histbtn = ttk.Button(self.histogramPanel, text = histfile[ind+1:])
            histbtn.grid(row=len(self.histbtns)+4,column=1, sticky='wens', padx=10, pady=10 )
            self.histbtns.append(histbtn)
            self.histfiles.append(histfile)
            if(len(self.histfiles)>=1):
                self.histbtn['state']='normal'
        

