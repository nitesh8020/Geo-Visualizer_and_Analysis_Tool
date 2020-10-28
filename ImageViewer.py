import tkinter as tk
from tkinter import ttk
from PIL import Image
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
        imgr = Image.open(self.file1)
        imgg = Image.open(self.file2)
        imgb = Image.open(self.file3)

        # Code to preview image comes here.
        red_img = np.array(imgr)
        red_array = red_img
        # green_array = np.array(imgg)
        # blue_array = np.array(imgb)

        # for i in range(len(red_array)):
        #     for j in range(len(red_array[i])):
        #         red_array[i][j][1] = green_array[i][j][1]
        #         red_array[i][j][2] = blue_array[i][j][2]
        
        img_full = Image.fromarray(red_array)
        self.figure = Figure(figsize = (10,6), dpi = 100)
        self.plot = self.figure.add_subplot(1,1,1)
        self.plot.imshow(img_full)
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