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
        self.set_resizable(0)
                
        grid = Gtk.Grid()
        self.add(grid)
                
        usrLabel = Gtk.Label("Benutzername")
                
        usrEntry = Gtk.Entry()
        usrEntry.set_text("Moritz Dan Noel")
                
        pwdLabel = Gtk.Label("Passwort")
                
        pwdEntry = Gtk.Entry()
        pwdEntry.set_text("********")
        pwdEntry.set_visibility(0)
        pwdEntry.set_invisible_char("*")

        loginButton = Gtk.Button(label = "Login")
        loginButton.connect("clicked", self.on_loginButton_clicked)
        
        quitButton = Gtk.Button(label = "Abbrechen")
        quitButton.connect("clicked", self.on_quitButton_clicked)
 
        grid.attach(usrLabel,1,1,1,1)
        grid.attach_next_to(usrEntry,usrLabel, Gtk.PositionType.BOTTOM,1,1)
        grid.attach_next_to(pwdLabel,usrLabel, Gtk.PositionType.RIGHT,1,1)
        grid.attach_next_to(pwdEntry,usrEntry, Gtk.PositionType.RIGHT,1,1)
        grid.attach_next_to(loginButton,usrEntry, Gtk.PositionType.BOTTOM,1,1)
        grid.attach_next_to(quitButton,loginButton, Gtk.PositionType.RIGHT,1,1)

    def on_loginButton_clicked(self,widget):
       # out_queue.put(StatusMessage("host: %s, pwd: %s", % usrEntry.get_text() , % pwdEntry.get_text())
        print("login happened")

    def on_quitButton_clicked(self,widget):
        self.destroy()
