#!/usr/bin/env python3
#from AddFrame import *
from . import AddFrame
#from MainFrame import *
from . import MainFrame

def main(in_queue, out_queue):
    mainframe = MainFrame() #MainFrame(root)
    mainframe.connect("delete-event", Gtk.main_quit)
    mainframe.show_all()
    addframe = AddFrame()
    addframe.connect("delete-event", Gtk.main_quit)
    addframe.show_all()
    Gtk.main()
