#!/usr/bin/env python3
#import tkinter as tk
#from tkinter import *
#from tkinter import ttk
#from tkinter.filedialog import askopenfilename, askopenfile
#from tkinter.messagebox import showerror
from AddFrame import *
#from Tktable import tktable

from gi.repository import Gtk

class MainFrame(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="GtkWin")

#        self.topwin.connect("delete-event", Gtk.main_quit)

#        self.topwin.title("topwin")
#        self.topwin.columnconfigure(5, weight = 1)
#        self.topwin.rowconfigure(5, weight = 1)
#        self.topwin.geometry('{}x{}'.format(500, 300))
# XXX SHITS NOT WORKING MAN!!!
#        self.topwin.grid(column=1)#(sticky = (N,W,E,S))


        self.search = Gtk.Button(label = "...")
        self.search.connect("clicked", self.load_file)
        self.add(self.search)

#        self.search.grid(column = 2, row = 2, sticky = W)

#        self.searchEntry = StringVar()
#        self.searchEntry = ttk.Entry(self.topwin, width = 30, textvariable=self.searchEntry)
#        self.searchEntry.grid(column = 1, row = 2, sticky = W)

#        ttk.Label(self.topwin, text = "File to analyse:").grid(column = 1, row = 1, sticky = W) 

#        self.add_task = Button(self.topwin, text="add", command = self.add_task_f, width=2, height=2)	
#        self.add_task.grid(column = 3, row = 3, sticky = W)

#        self.params = tktable.ArrayVar(self.topwin)
#        for y in range(6):
#            for x in range(6):
#                index = "%i,%i" % (y, x)
#                self.params[index] = index

#        self.table = tktable.Table(self.topwin,
#            rows = 6, cols = 6,
#            state = 'disabled',
#            width = 6, height = 6,
#            titlerows = 1, titlecols = 0,
#            roworigin = 0, colorigin = 0,
#            selectmode = 'browse', selecttype = 'row',
#            rowstretch = 'unset', colstrech = 'last',
#            flashmode = 'on',
#            variable = self.params)
#        self.table.pack(expand = 1, fill = 'both')
#        self.table.tag_configure('sel', background = 'yellow')
#        self.table.tag_configure('active', background = 'blue')
#        self.table.tag_configure('title', anchor = 'w', bg = 'red', relief = 'sunken')

    def load_file(self):
        fname = askopenfilename()

        if fname:
            try:
                print("""self.settings["template"].set(fname)""")
            except:
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
            return

    def add_task_f(self):
        self.add_task.config(state=DISABLED)
        self.addwin = Toplevel()
        self.addwin.wm_protocol("WM_DELETE_WINDOW", lambda:self.addwin_cancel())
        self.addwin.okay = Button(self.addwin, text="OK", command=self.addwin_ok, width=2, height=2)
        self.addwin.okay.grid(row=1, column=1)
        self.addwin.cancel = Button(self.addwin, text="Cancel", command=self.addwin_cancel, width=2, height=2)
        self.addwin.cancel.grid(row=1, column=2)


    def addwin_ok(self):
        # daten in scheduler hinzufugen
        self.add_task.config(state=NORMAL)
        self.addwin.destroy()

    def addwin_cancel(self):
        if messagebox.askokcancel("Quit", "Close without change?"):
            self.add_task.config(state=NORMAL)
            self.addwin.destroy()

