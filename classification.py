'''classification.py processes the image through image segmentation and then performs classification
Image segmentation is done through k means
Main libraries used are tkinter, pandas, sklearn, skimage, earthpy and matplotlib'''



import tkinter as tk
from tkinter import ttk
import os
import numpy as np
from tkinter import filedialog
import statistics as st
import pandas as pd
from sklearn.cluster import KMeans
from skimage.io import imread
import earthpy.plot as ep
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import warnings
warnings.filterwarnings('ignore')

# define class segmentation
class segmentation(ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.master = master
        self.display=ttk.Frame(self)
        self.createWidgets()
        self.files=[]

    def create(self):                       # create the main frame and k means image segmentation program
        if self.display.winfo_exists():
            self.display.grid_forget()
            self.display.destroy()
            
        self.display = ttk.Frame(self)
        self.display.grid(row = 0, column = 4,rowspan=2, sticky = 'nwes')
        frame=self.display
        
        file=self.files[0]
        image = imread(file) / 255
        l,b,c = image.shape

        nclusters = int(self.clusterInput.get())
        rescale_image = image.reshape(l*b,c)
        kmeans = KMeans(n_clusters=nclusters, random_state=0).fit(rescale_image)
        clustered = kmeans.cluster_centers_[kmeans.labels_]
        final_image = clustered.reshape(image.shape[0], image.shape[1], 3)
        self.figure = Figure(figsize = (6,4), dpi = 100)
        self.plot = self.figure.add_subplot(1,1,1)
        self.plot.imshow(final_image)
        self.canvas = FigureCanvasTkAgg(self.figure,frame)
        self.toolbar = NavigationToolbar2Tk(self.canvas,frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack()


    def createWidgets(self):                               # Create Widgets for frame
        self.grid_columnconfigure(0,weight = 0)
        self.grid_columnconfigure(1,weight = 1)
        
        self.grid_rowconfigure(0,weight = 0)
        self.grid_rowconfigure(1,weight = 1)

        self.panel = ttk.Frame(self)
        self.panel.grid(row=1, column=0, sticky='nsew')

        self.down = ttk.Frame(self) 
        self.down.grid(row = 2, column = 0, sticky = 'sw', columnspan = 4)
        
        self.txt = ttk.Label(self.panel, text="K-Means Segmentation", font="Arial 15 bold")
        self.txt.grid(row=0, column=0,sticky='wens', padx=10, pady=10)

        self.clusterLabel = ttk.Label(self.panel, text = "Enter number of clusters : ")
        self.clusterLabel.grid(row=1, column=0, sticky = 'nsew', padx = 10, pady = 10)

        self.clusterInput = ttk.Entry(self.panel)
        self.clusterInput.grid(row=2, column=0, sticky = 'nsew', padx = 10, pady = 10)
        
        self.btn = ttk.Button(self.panel, text='Choose Image', command=self.choose)
        self.btn.grid(row=3, column=0, sticky='nsew', padx=10, pady=10)

        self.createbtn = tk.Button(self.down, text='CREATE SEGMENTATION',bg='green', fg='white', command=self.create, state='disabled')
        self.createbtn.grid(row=4, column=0, sticky='nsew', padx=10, pady=10, columnspan=1)



    def choose(self, event=None):            # event handler for choose file
        ffile = filedialog.askopenfilename()
        if(ffile!=() and ffile!=''):
            ind= ffile.rfind('/')
            btn = ttk.Button(self.panel, text = ffile[ind+1:])
            btn.grid(row=4,column=0, sticky='nsew', padx=10, pady=10 )
            self.files.append(ffile)
            self.createbtn['state']='normal'