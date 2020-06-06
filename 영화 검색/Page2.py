from tkinter import *
from tkinter import font
import tkinter.ttk
from io import BytesIO
from PIL import Image, ImageTk
import tkinter.messagebox
from Set_xml import *

class Page2:
    def __init__(self,window):
        self.window = window
        self.fontstyle1 = font.Font(self.window, size=12, family='Consolas')
        self.fontstyle2 = font.Font(self.window, size=11, weight='bold', family='Consolas')
        self.Topfontstyle = font.Font(self.window, size=18, weight='bold', family='Consolas')
        self.set_xml = Set_xml()