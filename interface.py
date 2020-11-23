from tkinter import ttk
from ttkthemes import ThemedStyle
from glob import glob
import tkinter as tk
import rasterio as rio
from rasterio.plot import plotting_extent
import geopandas as gdp
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
from earthpy.io import path_to_example
from tkinter import filedialog
import matplotlib
import numpy as np
from ImageViewer import ViewImage
from Process import Process
import os
from Indices import Index
from datetime import datetime
from classification import segmentation
#clip file
# from clipmosaic import clipping


class RootFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title("Geo-Visualizer And Analysis Tool")        # title bar
        self.file1=''               # contains the contents of the data file
        self.file2=''
        self.file3=''
        self.pack(fill=tk.BOTH, expand=1)
        self.window=tk.Frame(self)
        self.createWidgets()            # call to create widgets
        
    def createWidgets(self):

        self.grid_columnconfigure(0,weight=0)
        self.grid_columnconfigure(1,weight=0)
        self.grid_columnconfigure(2,weight=0)
        self.grid_columnconfigure(3,weight=1)


        self.grid_rowconfigure(0,weight=0)
        self.grid_rowconfigure(1,weight=1)
            
        
        self.panel=ttk.Frame(self)
        self.panel.grid(row=0, column=0, sticky='nsew')
        
        self.menuBtn1 = ttk.Button(self.panel, text="Input", command=self.getInput)
        self.menuBtn1.grid(row=0, column=0)
        
        self.menuBtn2 = ttk.Button(self.panel, text="Process", command=self.Process)
        self.menuBtn2.grid(row=0, column=1)
        
        self.menuBtn3 = ttk.Button(self.panel, text="Index", command=self.calIndex)
        self.menuBtn3.grid(row=0, column=2)

        #$
        self.menuBtn4 = ttk.Button(self.panel, text="Clip Mosaic", command=self.clipping)
        self.menuBtn4.grid(row=0, column=3)
        #$

        self.menuBtn5 = ttk.Button(self.panel, text="Classification", command=self.segmentation)
        self.menuBtn5.grid(row=0, column=4)
        
        self.header = ttk.Label(self, text="",font="Arial 15 bold")
        self.header.grid(row=0, column=5)
        
        self.getInput()

                
    def getInput(self, event=None):
        if self.window.winfo_exists():
            self.window.grid_forget()
            self.window.destroy()
        self.header['text'] = 'Input'
        self.window = ViewImage(self)
        self.window.grid(row=1, column=0, columnspan=4, sticky='nsew')
        
        
    def Process(self, event=None):
        if self.window.winfo_exists():
            self.window.grid_forget()
            self.window.destroy()
        self.header['text'] = 'Process'
        self.window = Process(self)
        self.window.grid(row=1, column=0, columnspan=4, sticky='nsew')
    #$
    def clipping(self, event=None):
        if self.window.winfo_exists():
            self.window.grid_forget()
            self.window.destroy()
        self.header['text'] = 'Clipping'
        self.window = clipping(self)
        self.window.grid(row=1, column=0, columnspan=4, sticky='nsew')
    #$
    
    def segmentation(self, event=None):
        if self.window.winfo_exists():
            self.window.grid_forget()
            self.window.destroy()
        self.header['text'] = 'Image Segmentation'
        self.window = segmentation(self)
        self.window.grid(row=1, column=0, columnspan=4, sticky='nsew')

    
    def calIndex(self, event=None):
        if self.window.winfo_exists():
            self.window.grid_forget()
            self.window.destroy()
        self.header['text'] = 'Indices'
        self.window = Index(self)
        self.window.grid(row=1, column=0, columnspan=4, sticky='nsew')



root=tk.Tk()
root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='./icon/globe.png'))
root.geometry("1200x600")
root.configure(background='#eff0f1')
style=ThemedStyle(root)
style.set_theme('breeze')
style.configure('TButton', foreground = 'black')


my_gui = RootFrame(root)


root.mainloop()
