#!/usr/bin/env python3
#import tkinter as tk
#from tkinter import *
#from tkinter import ttk
#from tkinter.filedialog import askopenfilename, askopenfile
#from tkinter.messagebox import showerror
from AddFrame import *
from MainFrame import *
#from Tktable import tktable


if __name__ == "__main__":
    #mainframe = MainFrame() #MainFrame(root)
    #mainframe.connect("delete-event", Gtk.main_quit)
    #mainframe.show_all()
    mainframe = AddFrame()
    mainframe.connect("delete-event", Gtk.main_quit)
    mainframe.show_all()
    Gtk.main()
