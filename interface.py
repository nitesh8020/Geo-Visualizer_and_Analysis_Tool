'''Main file to implement all the functions and creating the main GUI
To run the main program, run this file'''


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
from clipmosaic import clipping
# from clipmosaic import clipping


class RootFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title("Geo-Visualizer And Analysis Tool")        # title bar
        self.pack(fill=tk.BOTH, expand=1)
        self.window=tk.Frame(self)
        self.menubtns=[]

        self.sn = ttk.Style()
        self.sn.configure('Emergency.TButton', font=('Helvetica', 12, 'bold'))
        
        
        self.createWidgets() 
        
        
    def createWidgets(self):            # create widgets

        self.grid_columnconfigure(0,weight=0)
        self.grid_columnconfigure(1,weight=0)
        self.grid_columnconfigure(2,weight=0)
        self.grid_columnconfigure(3,weight=1)


        self.grid_rowconfigure(0,weight=0)
        self.grid_rowconfigure(1,weight=1)
            
        
        self.panel=ttk.Frame(self)
        self.panel.grid(row=0, column=0, sticky='nsew')

        # Buttons to navigate between frames
        self.menuBtn1 = ttk.Button(self.panel, text="Feed Data", command=self.getInput)
        
        self.menuBtn1 = ttk.Button(self.panel, text="Create RGB image", command=self.getInput)
        self.menuBtn1.grid(row=0, column=0)
        self.menubtns.append(self.menuBtn1)
        

        self.menuBtn2 = ttk.Button(self.panel, text="Analysis", command=self.Process)
        self.menuBtn2 = ttk.Button(self.panel, text="Mosaic & Histogram", command=self.Process)

        self.menuBtn2.grid(row=0, column=1)
        self.menubtns.append(self.menuBtn2)
        
        self.menuBtn3 = ttk.Button(self.panel, text="Compute Indices", command=self.calIndex)
        self.menuBtn3.grid(row=0, column=2)
        self.menubtns.append(self.menuBtn3)

        self.menuBtn4 = ttk.Button(self.panel, text="Clip Mosaic", command=self.clipping)
        self.menuBtn4.grid(row=0, column=3)

        self.menuBtn5 = ttk.Button(self.panel, text="Classify Data", command=self.segmentation)
        self.menuBtn5.grid(row=0, column=4)

        #$
        # self.menuBtn4 = ttk.Button(self.panel, text="Clip Mosaic", command=self.clipping)
        # self.menuBtn4.grid(row=0, column=3)
        # self.menubtns.append(self.menuBtn4)
        #$

        self.menuBtn5 = ttk.Button(self.panel, text="Classification", command=self.segmentation)
        self.menuBtn5.grid(row=0, column=3)
        self.menubtns.append(self.menuBtn5)
        
        self.header = ttk.Label(self, text="",font="Arial 15 bold")
        self.header.grid(row=0, column=3)
        
        
        
        self.getInput()
        self.set(0)
        
    def set(self, ind):
        for btn in self.menubtns:
            btn['style']='my.TButton'
        self.menubtns[ind]['style']='Emergency.TButton'

                
    def getInput(self, event=None):             # Function for Getting input and displaying image using ViewImage.py'
        if self.window.winfo_exists():
            self.window.grid_forget()
            self.window.destroy()
        self.header['text'] = 'Feed Input Data Here'
        self.window = ViewImage(self)
        self.window.grid(row=1, column=0, columnspan=4, sticky='nsew')
        self.set(0)
        
        
    def Process(self, event=None):              # Function to implement Process.py for analysing and process.py
        if self.window.winfo_exists():
            self.window.grid_forget()
            self.window.destroy()
        self.header['text'] = 'Analysis and Processing of data'
        self.window = Process(self)
        self.window.grid(row=1, column=0, columnspan=4, sticky='nsew')
    

    def clipping(self, event=None):             # Function to Clip the mosaic using 'clipping.py'
        self.set(1)
    #$
    def clipping(self, event=None):
        if self.window.winfo_exists():
            self.window.grid_forget()
            self.window.destroy()
        self.header['text'] = 'Clip the Mosaic Image'
        self.window = clipping(self)
        self.window.grid(row=1, column=0, columnspan=4, sticky='nsew')
        self.set(3)
    #$
    
    
    def segmentation(self, event=None):         #Function to classify processed image image segmentation
        if self.window.winfo_exists():
            self.window.grid_forget()
            self.window.destroy()
        self.header['text'] = 'Image Segmentation'
        self.window = segmentation(self)
        self.window.grid(row=1, column=0, columnspan=4, sticky='nsew')
        self.set(4)

    
    def calIndex(self, event=None):             #   Function to compute indices using 'Index.py'
        if self.window.winfo_exists():
            self.window.grid_forget()
            self.window.destroy()
        self.header['text'] = 'Compute Indices'
        self.window = Index(self)
        self.window.grid(row=1, column=0, columnspan=4, sticky='nsew')
        self.set(2)



root=tk.Tk()
root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='./icon/globe.png'))
root.geometry("1200x600")

style=ThemedStyle(root)
themes=[]
for th in open('./themes.txt').readlines():themes.append(th.strip())
theme=open('./settings.txt').readlines()[0].split(' ')[1].strip()
if(theme not in themes): theme='breeze'
style.set_theme(theme)

my_gui = RootFrame(root)


root.mainloop()
