import tkinter as tk
from tkinter import ttk
import os
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog

import warnings
warnings.filterwarnings('ignore')

class segmentation(ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.master = master
        self.display=ttk.Frame(self)
        self.createWidgets()

    def createWidgets(self):
        self.grid_columnconfigure(0,weight = 0)
        self.grid_columnconfigure(1,weight = 1)
        
        self.grid_rowconfigure(0,weight = 0)
        self.grid_rowconfigure(1,weight = 1)

        self.panel = ttk.Frame(self)
        self.panel.grid(row=1, column=0, sticky='nsew')
