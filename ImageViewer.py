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
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import os
from datetime import datetime

class ViewImage(ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.master = master
        self.file1 =''
        self.file2 =''
        self.file3 =''
        self.createWidgets()


    def showImage(self):
        # directory = os.getcwd()
        # now = datetime.now()
        # dt_string = now.strftime("%d_%m_%Y_%H:%M:%S")
        # outdir = directory + '/img_STACK' + dt_string + '.tiff'
        outdir = 'OutputImages/'+self.out_name.get() + '.tiff'
        frame=self.frame
        self.band_fnames = [self.file1,self.file2,self.file3]
        arr_st, meta = es.stack(self.band_fnames, out_path = outdir, nodata = 0)
        self.figure = Figure(figsize = (10,6), dpi = 100)
        self.plot = self.figure.add_subplot(1,1,1)
        ep.plot_rgb((arr_st), stretch=True, str_clip = 0.5 , ax = self.plot)
        self.canvas = FigureCanvasTkAgg(self.figure,frame)
        self.toolbar = NavigationToolbar2Tk(self.canvas,frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack()

    def createWidgets(self):
        self.grid_columnconfigure(0,weight = 0)
        self.grid_columnconfigure(1,weight = 1)
        
        self.grid_rowconfigure(0,weight = 1)
        self.grid_rowconfigure(1,weight = 0)
        
        self.frame = tk.Frame(self)
        self.frame.grid(row = 0, column = 1, sticky = 'nwes')

        
        self.chooseButtons = ttk.Frame(self)
        self.chooseButtons.grid(row = 1, column = 0, padx = 5, pady = 5)

        self.choose_button1 = ttk.Button(self.chooseButtons, text="Red File", command = self.ChooseFileAction1)
        self.choose_button1.grid(row=1, column=0, padx=5, pady=5)

        self.choose_button2 = ttk.Button(self.chooseButtons, text="Green File", command = self.ChooseFileAction2)
        self.choose_button2.grid(row=1, column=1, padx=5, pady=5)

        self.choose_button3 = ttk.Button(self.chooseButtons, text="Blue File", command = self.ChooseFileAction3)
        self.choose_button3.grid(row=1, column=2, padx=5, pady=5)

        self.file_name_entry_Label = ttk.Label(self.chooseButtons, text="Output File Name")
        self.file_name_entry_Label.grid(row=2,column=0,padx=5,pady=5)

        self.out_name = ttk.Entry(self.chooseButtons)
        self.out_name.grid(row = 2, column = 1, padx = 5, pady = 5)
        
        
        

        

        self.show_image = ttk.Button(self, text="Show Image", command = self.showImage)
        self.show_image.grid(row=1, column=1, pady=10,padx=10, sticky='e')
        
        
        
        


    def ChooseFileAction1(self, event=None):			# event handler for choose file
        self.file1 = filedialog.askopenfilename()
        if(self.file1!=() and self.file1!=''):
            ind= self.file1.rfind('/')
            self.choose_button1["text"]='Red: '+self.file1[ind+1:]
        else: self.file1=''


    def ChooseFileAction2(self, event=None):			# event handler for choose file
        self.file2 = filedialog.askopenfilename()
        if(self.file2!=() and self.file2!=''):
            ind= self.file2.rfind('/')
            self.choose_button2["text"]='Green: '+self.file2[ind+1:]
        else: self.file2=''

    def ChooseFileAction3(self, event=None):			# event handler for choose file
        self.file3 = filedialog.askopenfilename()
        if(self.file3!=() and self.file3!=''):
            ind= self.file3.rfind('/')
            self.choose_button3["text"]='Blue: '+self.file3[ind+1:]
        else: self.file3=''

        

