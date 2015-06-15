#!/usr/bin/env python3
# coding: utf8

from . import addframe
from . import mainframe
from . import sshframe
from gi.repository import Gtk

def main(in_queue, out_queue):
    mf = mainframe.MainFrame(in_queue, out_queue) #MainFrame(root)
    mf.connect("delete-event", Gtk.main_quit)
    mf.show_all()

    af = addframe.AddFrame(in_queue,out_queue)
    af.connect("delete-event", Gtk.main_quit)
    af.show_all()
    
    sf = sshframe.SshFrame(in_queue,out_queue)
    sf.connect("delete-event", Gtk.main_quit)
    sf.show_all()

    Gtk.main()
    
if __name__ == "__main__":
    test = main(in_queue,out_queue)

