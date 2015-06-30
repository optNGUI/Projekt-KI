# coding: utf8

import logging
from .main import send_msg
from .. import util
from gi.repository import Gtk

__pwdEntry = None
__usrEntry = None

class SshFrame(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self,title = "ssh-Gate")      

        self.set_default_size(200,90)
        self.set_border_width(10)
        self.set_resizable(0)
        
        global __pwdEntry
        global __usrEntry
        
        grid = Gtk.Grid()
        self.add(grid)
                
        usrLabel = Gtk.Label("Host")
                
        __usrEntry = Gtk.Entry()
        __usrEntry.set_text("616863@ssh-gate.uni-luebeck.de")
                
        pwdLabel = Gtk.Label("Passwort")
                
        __pwdEntry = Gtk.Entry()
        __pwdEntry.set_text("abc01354")
        __pwdEntry.set_visibility(0)
        __pwdEntry.set_invisible_char("*")

        loginButton = Gtk.Button(label = "Login")
        loginButton.connect("clicked", self.on_loginButton_clicked)
        
        quitButton = Gtk.Button(label = "Abbrechen")
        quitButton.connect("clicked", self.on_quitButton_clicked)
 
        grid.attach(usrLabel,1,1,1,1)
        grid.attach_next_to(__usrEntry,usrLabel, Gtk.PositionType.BOTTOM,1,1)
        grid.attach_next_to(pwdLabel,usrLabel, Gtk.PositionType.RIGHT,1,1)
        grid.attach_next_to(__pwdEntry,__usrEntry, Gtk.PositionType.RIGHT,1,1)
        grid.attach_next_to(loginButton,__usrEntry, Gtk.PositionType.BOTTOM,1,1)
        grid.attach_next_to(quitButton,loginButton, Gtk.PositionType.RIGHT,1,1)

    def on_loginButton_clicked(self,widget):
        send_msg(util.CommandMessage(content = 'password:  {msg}'.format(msg = __pwdEntry.get_text())))
        send_msg(util.CommandMessage(content = 'set config SSH host  {msg}'.format(msg = __usrEntry.get_text())))
        print('ssh schickt weg')
        self.destroy()

    def on_quitButton_clicked(self,widget):
        self.destroy()
    
