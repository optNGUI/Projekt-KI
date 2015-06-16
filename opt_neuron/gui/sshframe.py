#!/usr/bin/env python3
# coding: utf8

from gi.repository import Gtk

class SshFrame(Gtk.Window):
    def __init__(self,in_queue,out_queue):
        Gtk.Window.__init__(self,title = "Ssh-Gate")
        self.in_queue = in_queue
        self.out_queue = out_queue

        self.set_default_size(200,90)
        self.set_border_width(10)
                
        grid = Gtk.Grid()
        self.add(grid)
                
        usrLabel = Gtk.Label("Benutzername")
                
        usrEntry = Gtk.Entry()
        usrEntry.set_text("Moritz Dann Nöhl")
                
        pwdLabel = Gtk.Label("Passwort")
                
        pwdEntry = Gtk.Entry()
        pwdEntry.set_text("********")
        pwdEntry.set_invisible(0)
        pwdEntry.set_invisible_char("*")
                
        grid.attach(usrLabel,1,1,1,1)
        grid.attach_next_to(usrEntry,usrLabel, Gtk.PositionType:BOTTOM,1,1)
        grid.attach_next_to(pwdLabel,usrEntry, Gtk.PositionType:BOTTOM,1,1)
        grid.attach_next_to(pwdEntry,pwdLabel, Gtk.PositionType:BOTTOM,1,1)