
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

import warnings
warnings.filterwarnings('ignore')

fields = ('x_min', 'y_min', 'x_max', 'y_max')
out_tif = "clipped_mosaic.tif"
class clipping(ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.master = master
        self.msfile=''   #mosaic file
        self.display=ttk.Frame(self)
        self.createWidgets()
        ents = makeform(root, fields)

    def createWidgets(self):
        self.grid_columnconfigure(0,weight = 0)
        self.grid_columnconfigure(1,weight = 1)
        
        self.grid_rowconfigure(0,weight = 0)
        self.grid_rowconfigure(1,weight = 1)

        self.panel = ttk.Frame(self)
        self.panel.grid(row=1, column=0, sticky='nsew')
        
        #mosaicfile selection button
        self.msbtn = tk.Button(self, text='select Mosaicfile', command=self.mosaicfile)
        self.msbtn.grid(row=3, column=0, sticky='nsew', padx=10, pady=10)
        
        #clipping button
        self.cpbtn = tk.Button(self, text='clip mosaic', command=(lambda e=ents: self.ClipImage(e)))
        self.cpbtn.grid(row=4, column=0, sticky='nsew', padx=10, pady=10)

    
    def mosaicfile(self, event=None):
        self.msfile = filedialog.askopenfilename()
        if(self.msfile!=() and self.msfile!=''):
            ind= self.msfile.rfind('/')
            self.msbtn["text"]='shape: '+self.msfile[ind+1:]
        else: self.msfile=''

    def ClipImage(entries):
        if self.display.winfo_exists():
            self.display.grid_forget()
            self.display.destroy()
            
        self.display = ttk.Frame(self)
        self.display.grid(row = 0, column = 1,rowspan=2, sticky = 'nwes')
        
        x_min = float(entries['x_min'].get())
        y_min = float(entries['x_min'].get())
        x_max = float(entries['x_min'].get())
        y_max = float(entries['x_min'].get())
        
        #mosaic file
        soap_chm_path = self.msfile
        #shapefile
        dataset = gdal.Open(fp)
        band = dataset.GetRasterBand(1)
    
        geotransform = dataset.GetGeoTransform()

        arr = band.ReadAsArray()
        plt.imshow(arr, cmap='terrain')
        def mouse_move(event):
            x, y = event.xdata, event.ydata


        plt.connect('motion_notify_event', mouse_move)
    
        plt.axis('equal')
        plt.show()

        
        with rasterio.open(soap_chm_path) as src:
        #window = Window(padding, padding, src.width - 2 * padding, src.height - 2 * padding)
            window = Window(x_min,y_min,x_max,y_max)
        
            kwargs = src.meta.copy()
            kwargs.update({'height': window.height, 'width': window.width, 'transform': rasterio.windows.transform(window, src.transform)})

            with rasterio.open(out_tif, 'w', **kwargs) as dst:
                dst.write(src.read(window=window))

    def makeform(root, fields):
        entries = {}
        for field in fields:
            print(field)
            row = tk.Frame(root)
            lab = tk.Label(row, width=22, text=field+": ", anchor='w')
            ent = tk.Entry(row)
            ent.insert(0, "0")
            row.pack(side=tk.TOP,fill=tk.X,padx=5,pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries[field] = ent
    return entries
