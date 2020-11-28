
import tkinter as tk
from tkinter import ttk
import rasterio
import os
import numpy as np
import rasterio as rio
from rasterio.plot import show
from rasterio.mask import mask
from shapely.geometry import mapping
import matplotlib.pyplot as plt
import geopandas as gpd
import earthpy as et
import earthpy.plot as ep
import earthpy.spatial as es
import cartopy as cp
from tkinter import filedialog
from osgeo import gdal
from matplotlib.backends.backend_tkagg import (NavigationToolbar2Tk)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvas
from rasterio.windows import Window
import warnings
warnings.filterwarnings('ignore')

#out_tif = "clipped_mosaic.tif"

class clipping(ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.master = master
        self.msfile=''   #mosaic file
        self.display=ttk.Frame(self)
        self.createWidgets()
        
    def show_image(self):
        if self.display.winfo_exists():
            self.display.grid_forget()
            self.display.destroy()
        
        self.display = ttk.Frame(self)
        self.display.grid(row = 0, column = 2, columnspan = 4, rowspan=3, sticky = 'nsew')
        frame=self.display
        
        fp = self.msfile
        self.fig = plt.Figure(figsize = (8,4), dpi =100)
        self.ax = self.fig.add_subplot(111)
        self.canvas_preview = FigureCanvas(self.fig, frame)
        
        
        self.dataset = gdal.Open(fp)
        self.band = self.dataset.GetRasterBand(1)
        self.geotransform = self.dataset.GetGeoTransform()
        self.arr = self.band.ReadAsArray()
        self.ax.imshow(self.arr, cmap='terrain')
        self.ax.axis('equal')
        self.ax.set(title="",xticks=[], yticks=[])
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["left"].set_visible(False)
        self.ax.spines["bottom"].set_visible(False)

        self.canvas_preview.draw()
        self.fig.subplots_adjust(left=0.0, bottom=0.0, right=1.0, top=1.0)

        #self.canvas_preview.get_tk_widget().pack(side='top', fill='both', expand = 1)
        self.toolbar = NavigationToolbar2Tk(self.canvas_preview, frame)
        self.toolbar.update()
        self.canvas_preview.get_tk_widget().pack(side='top', fill='both', expand = 1)
        
    def show_clipped_image(self):
        if self.display.winfo_exists():
            self.display.grid_forget()
            self.display.destroy()
        
        self.display = ttk.Frame(self)
        self.display.grid(row = 0, column = 2, columnspan = 4, rowspan=3, sticky = 'nsew')
        frame=self.display
        
        fp = self.msfile
        self.fig = plt.Figure(figsize = (8,4), dpi =100)
        self.ax = self.fig.add_subplot(111)
        self.canvas_preview = FigureCanvas(self.fig, frame)
        
        fp = self.outname.get()+'.tif'
        self.dataset = gdal.Open(fp)
        self.band = self.dataset.GetRasterBand(1)
        self.geotransform = self.dataset.GetGeoTransform()
        self.arr = self.band.ReadAsArray()
        self.ax.imshow(self.arr, cmap='terrain')
        self.ax.axis('equal')
        self.ax.set(title="",xticks=[], yticks=[])
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["left"].set_visible(False)
        self.ax.spines["bottom"].set_visible(False)

        self.canvas_preview.draw()
        self.fig.subplots_adjust(left=0.0, bottom=0.0, right=1.0, top=1.0)

        #self.canvas_preview.get_tk_widget().pack(side='top', fill='both', expand = 1)
        self.toolbar = NavigationToolbar2Tk(self.canvas_preview, frame)
        self.toolbar.update()
        self.canvas_preview.get_tk_widget().pack(side='top', fill='both', expand = 1)
        
    
        

    def createWidgets(self):
        self.grid_columnconfigure(0,weight = 0)
        self.grid_columnconfigure(1,weight = 1)
        
        self.grid_rowconfigure(0,weight = 0)
        self.grid_rowconfigure(1,weight = 1)

        self.panel = ttk.Frame(self)
        self.panel.grid(row=1, column=0, sticky='nsew')
        
        #mosaicfile selection button
        self.msbtn = ttk.Button(self.panel, text='select Mosaicfile', command=self.mosaicfile)
        self.msbtn.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        #show image
        self.showimage = ttk.Button(self.panel, text='Show Image', command = self.show_image)
        self.showimage.grid(row=1, column=0, sticky = 'nsew', pady = 10,padx = 10)
        #xmin
        self.InputLabe1 = ttk.Label(self.panel, text = "x min")
        self.InputLabe1.grid(row=2, column=0, sticky = 'nsew', padx = 10, pady = 10)

        self.InputXmin= ttk.Entry(self.panel)
        self.InputXmin.grid(row=3, column=0, sticky = 'nsew', padx = 10, pady = 10)
        
        #ymin
        self.InputLabe2 = ttk.Label(self.panel, text = "y min")
        self.InputLabe2.grid(row=4, column=0, sticky = 'nsew', padx = 10, pady = 10)

        self.InputYmin = ttk.Entry(self.panel)
        self.InputYmin.grid(row=5, column=0, sticky = 'nsew', padx = 10, pady = 10)
        
        #xmax
        self.InputLabe3 = ttk.Label(self.panel, text = "x max")
        self.InputLabe3.grid(row=6, column=0, sticky = 'nsew', padx = 10, pady = 10)

        self.InputXmax = ttk.Entry(self.panel)
        self.InputXmax.grid(row=7, column=0, sticky = 'nsew', padx = 10, pady = 10)
        
        #ymax
        self.InputLabe4 = ttk.Label(self.panel, text = "y max")
        self.InputLabe4.grid(row=8, column=0, sticky = 'nsew', padx = 10, pady = 10)

        self.InputYmax = ttk.Entry(self.panel)
        self.InputYmax.grid(row=9, column=0, sticky = 'nsew', padx = 10, pady = 10)
        
        #name of clipped image
        self.InputLabel5 = ttk.Label(self.panel, text = "enter image name")
        self.InputLabel5.grid(row=10, column=0, sticky = 'nsew', padx = 10, pady = 10)

        self.outname= ttk.Entry(self.panel)
        self.outname.grid(row=11, column=0, sticky = 'nsew', padx = 10, pady = 10)
        
        #clipping button
        #self.cpbtn = ttk.Button(self.panel, text='clip mosaic', command=(lambda e=ents: self.ClipImage(e)))
        self.cpbtn = ttk.Button(self.panel, text='clip mosaic', command=self.ClipImage)
        self.cpbtn.grid(row=12, column=0, sticky='nsew', padx=10, pady=10)
    
        self.showimage1 = ttk.Button(self.panel, text='Show Clipped Image', command = self.show_clipped_image)
        self.showimage1.grid(row=13, column=0, sticky = 'nsew', pady = 10,padx = 10)
    
    def mosaicfile(self, event=None):
        self.msfile = filedialog.askopenfilename()
        if(self.msfile!=() and self.msfile!=''):
            ind= self.msfile.rfind('/')
            self.msbtn["text"]='shape: '+self.msfile[ind+1:]
            #self.window.grid(row=1, column=0, columnspan=4, sticky='nsew')
        else: self.msfile=''
    
    def ClipImage(self):
        if self.display.winfo_exists():
            self.display.grid_forget()
            self.display.destroy()
            
        #self.display = ttk.Frame(self)
        #self.display.grid(row = 0, column = 1,rowspan=2, sticky = 'nwes')
        
        x_min = float(self.InputXmin.get())
        y_min = float(self.InputYmin.get())
        x_max = float(self.InputXmax.get())
        y_max = float(self.InputYmax.get())
        #out_path = 'OutputImages/'+self.entry.get()+'.tif'
        cfile = self.outname.get()+'.tif'
        with rasterio.open(self.msfile) as src:
        #window = Window(padding, padding, src.width - 2 * padding, src.height - 2 * padding)
            window = Window(x_min, y_min, x_max, y_max)
        
            kwargs = src.meta.copy()
            kwargs.update({'height': window.height, 'width': window.width, 'transform': rasterio.windows.transform(window, src.transform)})

            with rasterio.open(cfile, 'w', **kwargs) as dst:
                dst.write(src.read(window=window))
        
