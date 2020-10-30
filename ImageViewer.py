import tkinter as tk
from tkinter import ttk
from glob import glob
import rasterio as rio
from rasterio.plot import plotting_extent
import geopandas as gdp
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
import matplotlib
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class ViewImage(ttk.Frame):
    def __init__(self,master,file1,file2,file3):
        super().__init__(master)
        self.master = master
        self.file1 = file1
        self.file2 = file2
        self.file3 = file3
        self.grid(row = 1, column = 1, columnspan = 2, sticky = 'nsew',padx = 5, pady = 5)
        self.createWidgets()


    def showImage(self,frame):
        self.band_fnames = [self.file1,self.file2,self.file3]
        arr_st, meta = es.stack(self.band_fnames, nodata = -9999)
        self.figure = Figure(figsize = (10,6), dpi = 100)
        self.plot = self.figure.add_subplot(1,1,1)
        ep.plot_rgb((arr_st), stretch=True, str_clip = 0.5 , ax = self.plot)
        self.canvas = FigureCanvasTkAgg(self.figure,frame)
        self.toolbar = NavigationToolbar2Tk(self.canvas,frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack()

    def createWidgets(self):
        self.grid_columnconfigure(0,weight = 1)
        self.grid_rowconfigure(0,weight = 1)
        self.frame = ttk.Frame(self)
        self.showImage(self.frame)
        self.frame.grid(row = 0, column = 0, sticky = 'nwes')