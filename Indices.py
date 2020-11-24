'''Indices.py computes indices for the input tiff files
It also provides a way to manipulate the formula for calculating indices
Main libraries used are tkinter, rasterio, matplotlib and earthpy'''


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

# Define class
class Index(ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.master = master
        self.NIR=''
        self.R=''
        self.G=''
        self.B=''
        self.display=ttk.Frame(self)
        self.createWidgets()


    def create(self):                   # Funtion to cleate the main frame
        if self.display.winfo_exists():
            self.display.grid_forget()
            self.display.destroy()
            
        self.display = ttk.Frame(self)
        self.display.grid(row = 0, column = 2,rowspan=2, sticky = 'nwes')
        frame=self.display
        p=''
        g=1
        b=1
        nir=1
        r=1
        if(self.NIR!=''):
                nir=rasterio.open(self.NIR)
                nir=nir.read(1)
                nir=nir.astype(float)
                p=nir[...,np.newaxis].shape
                
        if(self.R!=''):
                r=rasterio.open(self.R)
                r=r.read(1)
                r=r.astype(float)
                p=r[...,np.newaxis].shape
                
        if(self.G!=''):
                g=rasterio.open(self.G)
                g=g.read(1)
                g=g.astype(float)
                p=g[...,np.newaxis].shape
                
        if(self.B!=''):
                b=rasterio.open(self.B)
                b=b.read(1)
                b=b.astype(float)
                p=b[...,np.newaxis].shape
		

        
        
        
        
        np.seterr(divide='ignore', invalid='ignore')
        self.calc=np.empty(p, dtype=rasterio.float32)
        check=nir*r*g*b>0
        cmd=self.entry.get()
        s='self.calc=np.where(check,{}, -999)'.format(cmd)
        exec(s, {'self':self,'np':np, 'nir':nir, 'r':r,'g':g,'b':b, 'check':check, 'sqrt':np.sqrt})
        self.figure = Figure(figsize = (6,4), dpi = 100)
        self.plot = self.figure.add_subplot(1,1,1)
        show(self.calc, cmap='summer', ax = self.plot)
        self.canvas = FigureCanvasTkAgg(self.figure,frame)
        self.toolbar = NavigationToolbar2Tk(self.canvas,frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack()
        self.saveImg(self.calc)
	
    def createNDVI(self):                   # Function to create NDVI
        if self.display.winfo_exists():
            self.display.grid_forget()
            self.display.destroy()
            
        self.display = ttk.Frame(self)
        self.display.grid(row = 0, column = 2,rowspan=2, sticky = 'nwes')
        frame=self.display
        nir=rasterio.open(self.NIR)
        nir=nir.read(1)
        r=rasterio.open(self.R)
        r=r.read(1)
        nir=nir.astype(float)
        r=r.astype(float)
        np.seterr(divide='ignore', invalid='ignore')
        self.ndvi=np.empty(r[..., np.newaxis].shape, dtype=rasterio.float32)
        check=np.logical_or(r>0, nir>0)
        self.ndvi=np.where(check, (nir-r)/(nir+r), -999)
        self.figure = Figure(figsize = (6,4), dpi = 100)
        self.plot = self.figure.add_subplot(1,1,1)
        show(self.ndvi, cmap='summer' , ax = self.plot)
        self.canvas = FigureCanvasTkAgg(self.figure,frame)
        self.toolbar = NavigationToolbar2Tk(self.canvas,frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack()
        self.saveImg(self.ndvi)
        # image_in = "ndviImage.tif"
        # image_out = "path_output_image.tif"
        # subprocess.call(["gdal_translate","-of","GTiff", "-ot", "Byte", "-scale", image_in, image_out ])

        

    def createWidgets(self):
        self.grid_columnconfigure(0,weight = 0)
        self.grid_columnconfigure(1,weight = 1)
        
        self.grid_rowconfigure(0,weight = 0)
        self.grid_rowconfigure(1,weight = 1)
        
        self.panel = ttk.Frame(self)
        self.panel.grid(row=1, column=0, sticky='nsew')
       

        self.btnNIR = ttk.Button(self.panel, text='NIR', command=self.chooseNIR)
        self.btnNIR.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        
        self.btnR = ttk.Button(self.panel, text='R', command=self.chooseR)
        self.btnR.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        
        self.btnG = ttk.Button(self.panel, text='G', command=self.chooseG)
        self.btnG.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)
        
        self.btnB = ttk.Button(self.panel, text='B', command=self.chooseB)
        self.btnB.grid(row=3, column=0, sticky='nsew', padx=10, pady=10)
                
        self.lbl = ttk.Label(self.panel, text='Enter formula: ')
        self.lbl.grid(row=4, column=0, sticky='nsew', padx=10, pady=10)
        
        self.entry = ttk.Entry(self.panel)
        self.entry.insert(0, '(nir-r)/(nir+r)')
        self.entry.grid(row=5, column=0, sticky='nsew', padx=10, pady=10)

        self.label = ttk.Label(self.panel, text = 'Enter Output File Name: ')
        self.label.grid(row = 6, column = 0, sticky = 'nsew', padx=10, pady=10)

        self.out_name = ttk.Entry(self.panel)
        self.out_name.grid(row = 7, column = 0, sticky = 'nsew', padx = 10, pady = 10)

        
        self.btnNDVI = ttk.Button(self.panel, text='NDVI', command=self.createNDVI)
        self.btnNDVI.grid(row=8, column=0, sticky='nsew', padx=10, pady=10)
        
        self.btncreate = ttk.Button(self.panel, text='Calculate Index from formula', command=self.create)
        self.btncreate.grid(row=9, column=0, sticky='nsew', padx=10, pady=10)
        
        
        
        
    def chooseNIR(self, event=None):            # event handler for choose file
        ffile = filedialog.askopenfilename()
        if(ffile!=() and ffile!=''):
            ind= ffile.rfind('/')
            self.btnNIR['text']='NIR: '+ffile[ind+1:]
            self.NIR=ffile
            
    def chooseR(self, event=None):            # event handler for choose file
        ffile = filedialog.askopenfilename()
        if(ffile!=() and ffile!=''):
            ind= ffile.rfind('/')
            self.btnR['text']='R: '+ffile[ind+1:]
            self.R=ffile
            
    def chooseG(self, event=None):            # event handler for choose file
        ffile = filedialog.askopenfilename()
        if(ffile!=() and ffile!=''):
            ind= ffile.rfind('/')
            self.btnG['text']='G: '+ffile[ind+1:]
            self.G=ffile
            
    def chooseB(self, event=None):            # event handler for choose file
        ffile = filedialog.askopenfilename()
        if(ffile!=() and ffile!=''):
            ind= ffile.rfind('/')
            self.btnB['text']='B: '+ffile[ind+1:]
            self.B=ffile

        
    def saveImg(self,name):                   # Function to save the image
        source = ''
        outputFile = 'OutputImages/' + self.out_name.get() + '.tiff'
        if (self.NIR!=''):
            source = self.NIR
        elif self.R!='':
            source = self.R
        elif self.G!='':
            source = self.G
        else:
            source = self.B
        src1 = rasterio.open(source)
        ndviImage = rasterio.open(outputFile,'w',driver='Gtiff',width=src1.width, height = src1.height, count=1, crs=src1.crs, transform=src1.transform, dtype='float64')
        ndviImage.write(name,1)
        ndviImage.close()
        
