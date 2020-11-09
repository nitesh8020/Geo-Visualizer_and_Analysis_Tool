# to explore clip
# one can download shapes and mosiac images from
# https://www.earthdatascience.org/workshops/gis-open-source-python/crop-raster-data-in-python/
# downloading section : Download spatial-vector-lidar data subset (~172 MB)
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

import warnings
warnings.filterwarnings('ignore')

class clipping(ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.master = master
        self.msfile=''   #mosaic file
        self.shfile=''   #shapefile to clip mosaic
        self.display=ttk.Frame(self)
        self.createWidgets()

    def createWidgets(self):
        self.grid_columnconfigure(0,weight = 0)
        self.grid_columnconfigure(1,weight = 1)
        
        self.grid_rowconfigure(0,weight = 0)
        self.grid_rowconfigure(1,weight = 1)

        self.panel = ttk.Frame(self)
        self.panel.grid(row=1, column=0, sticky='nsew')

    
        #shapefile selection button
        self.shbtn = tk.Button(self, text='select Shapefile', command=self.shapefile)
        self.shbtn.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)
        
        #mosaicfile selection button
        self.msbtn = tk.Button(self, text='select Mosaicfile', command=self.mosaicfile)
        self.msbtn.grid(row=3, column=0, sticky='nsew', padx=10, pady=10)
        
        #clipping button
        self.cpbtn = tk.Button(self, text='clip mosaic', command=self.ClipImage)
        self.cpbtn.grid(row=4, column=0, sticky='nsew', padx=10, pady=10)

    
    def shapefile(self, event=None):
        self.shfile = filedialog.askopenfilename()
        if(self.shfile!=() and self.shfile!=''):
            ind= self.shfile.rfind('/')
            self.shbtn["text"]='shape: '+self.shfile[ind+1:]
        else: self.shfile=''

    def mosaicfile(self, event=None):
        self.msfile = filedialog.askopenfilename()
        if(self.msfile!=() and self.msfile!=''):
            ind= self.msfile.rfind('/')
            self.msbtn["text"]='mosaic: '+self.msfile[ind+1:]
        else: self.msfile=''

    def ClipImage(self):
        if self.display.winfo_exists():
            self.display.grid_forget()
            self.display.destroy()
            
        self.display = ttk.Frame(self)
        self.display.grid(row = 0, column = 1,rowspan=2, sticky = 'nwes')
        
        ##
        #mosaic file
        soap_chm_path = self.msfile
        with rio.open(soap_chm_path) as src:
            lidar_chm_im = src.read(masked=True)[0]
            extent = rio.plot.plotting_extent(src)
            soap_profile = src.profile
        #shapefile
        crop_extent_soap = gpd.read_file(self.shfile)

        fig, ax = plt.subplots(figsize=(10, 10))
        ep.plot_bands(lidar_chm_im,cmap='terrain',extent=extent,ax=ax,cbar=False)
        crop_extent_soap.plot(ax=ax, alpha=.6, color='g');

        with rio.open(soap_chm_path) as src:
            lidar_chm_crop, soap_lidar_meta = es.crop_image(src,crop_extent_soap)

        # Update the metadata to have the new shape (x and y and affine information)
        soap_lidar_meta.update({"driver": "GTiff", "height": lidar_chm_crop.shape[0], "width": lidar_chm_crop.shape[1], "transform": soap_lidar_meta["transform"]})

        # generate an extent for the newly cropped object for plotting
        cr_ext = rio.transform.array_bounds(soap_lidar_meta['height'], soap_lidar_meta['width'], soap_lidar_meta['transform'])

        bound_order = [0,2,1,3]
        cr_extent = [cr_ext[b] for b in bound_order]
        cr_extent, crop_extent_soap.total_bounds

        # mask the nodata and plot the newly cropped raster layer
        lidar_chm_crop_ma = np.ma.masked_equal(lidar_chm_crop[0], -9999.0)
        ep.plot_bands(lidar_chm_crop_ma, cmap='terrain', cbar=False);
        #save output
        path_out = "clipped_image.tif"
        with rio.open(path_out, 'w', **soap_lidar_meta) as ff: ff.write(lidar_chm_crop[0], 1)

