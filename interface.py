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


class RootFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title("GPS Data Analysis")		# title bar
        self.file1=''               # contains the contents of the data file
        self.file2=''
        self.file3=''
        self.pack(fill=tk.BOTH, expand=1)
        self.window=tk.Frame(self)
        self.createWidgets()			# call to create widgets
		
    def createWidgets(self):

        self.grid_columnconfigure(0,weight=0)
        self.grid_columnconfigure(1,weight=1)
        self.grid_columnconfigure(2,weight=0)


        self.grid_rowconfigure(0,weight=0)
        self.grid_rowconfigure(1,weight=1)
        self.grid_rowconfigure(2,weight=0)
		# grid weights configure
		
        self.header = ttk.Label(self, text="Please choose the files...",font="Arial 25 bold")
        self.header.grid(row=0, column=0, columnspan=3)

        self.chooseButtons = ttk.Frame(self)
        self.chooseButtons.grid(row = 2, column = 2, padx = 5, pady = 5)

        self.choose_button1 = ttk.Button(self.chooseButtons, text="Red File", command = self.ChooseFileAction1)
        self.choose_button1.grid(row=2, column=0, padx=5, pady=5)

        self.choose_button2 = ttk.Button(self.chooseButtons, text="Green File", command = self.ChooseFileAction2)
        self.choose_button2.grid(row=2, column=1, padx=5, pady=5)

        self.choose_button3 = ttk.Button(self.chooseButtons, text="Blue File", command = self.ChooseFileAction3)
        self.choose_button3.grid(row=2, column=2, padx=5, pady=5)


        self.panel=ttk.Frame(self)
        self.panel.grid(row=1, column=0, sticky='w')

        self.show_image = ttk.Button(self, text="Show Image", command = self.ShowImage)
        self.show_image.grid(row=2, column=0, sticky='nsew', pady=10)

				
		
    def ShowImage(self, event = None):
        if self.window.winfo_exists():
            self.window.grid_forget()
            self.window.destroy()

        self.header['text'] = 'Image'
        if (self.file1!='' and self.file2!='' and self.file3!=''):
            self.window = ViewImage(self,self.file1,self.file2,self.file3)
        else:
            self.header['text'] = 'Please Choose all the files.'

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

        self.ShowImage()


root=tk.Tk()
root.geometry("1200x600")
root.configure(background='#eff0f1')
style=ThemedStyle(root)
style.set_theme('breeze')
style.configure('TButton', foreground = 'black')


my_gui = RootFrame(root)


root.mainloop()
