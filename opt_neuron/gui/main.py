#!/usr/bin/env python3
# coding: utf8

from . import addframe
from . import mainframe
from gi.repository import Gtk

def main(in_queue, out_queue):
    mf = mainframe.MainFrame(in_queue, out_queue) #MainFrame(root)
    mf.connect("delete-event", Gtk.main_quit)
    mf.show_all()

    af = addframe.AddFrame(out_queue)
    af.connect("delete-event", Gtk.main_quit)
    af.show_all()

    Gtk.main()

