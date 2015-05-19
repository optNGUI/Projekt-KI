#!/usr/bin/env python3
from AddFrame import *
from MainFrame import *

if __name__ == "__main__":
    mainframe = MainFrame() #MainFrame(root)
    mainframe.connect("delete-event", Gtk.main_quit)
    mainframe.show_all()
    addframe = AddFrame()
    addframe.connect("delete-event", Gtk.main_quit)
    addframe.show_all()
    Gtk.main()
