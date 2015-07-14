
import logging
from .main import send_msg, get_msg
from .. import util
from gi.repository import Gtk

__pwdEntry = None
__usrEntry = None
__netEntry = None
__analysisEntry = None
__parent = None

class SshFrame(Gtk.Window):
    def __init__(self, parent):
        Gtk.Window.__init__(self,title = "ssh-Gate")      

        self.set_default_size(200,140)
        self.set_border_width(10)
        self.set_resizable(0)
        self.connect("delete-event",self.on_xButton_clicked)
        
        global __pwdEntry
        global __usrEntry
        global __netEntry
        global __analysisEntry
        global __parent
        
        grid = Gtk.Grid()
        self.add(grid)
        
        __parent = parent
 
        usrLabel = Gtk.Label("Host")
                
        __usrEntry = Gtk.Entry()
        __usrEntry.set_text("bachelor1@localhost")
                
        pwdLabel = Gtk.Label("Passwort")
                
        __pwdEntry = Gtk.Entry()
        __pwdEntry.set_text("rdx556")
        __pwdEntry.set_visibility(0)
        __pwdEntry.set_invisible_char("*")

        netLabel = Gtk.Label("net")
        
        __netEntry = Gtk.Entry()
        __netEntry.set_text("cd ~/acnet2 && genesis acnet2.g")
        
        analysisLabel = Gtk.Label("analysis")
        
        __analysisEntry = Gtk.Entry()
        __analysisEntry.set_text("cd ~/acnet2 && python ./analysis.py")
        
        loginButton = Gtk.Button(label = "Login")
        loginButton.connect("clicked", self.on_loginButton_clicked)
        
        quitButton = Gtk.Button(label = "Abbrechen")
        quitButton.connect("clicked", self.on_quitButton_clicked)
 
        grid.attach(usrLabel,1,1,1,1)
        grid.attach_next_to(__usrEntry,usrLabel, Gtk.PositionType.BOTTOM,1,1)
        grid.attach_next_to(netLabel,__usrEntry, Gtk.PositionType.BOTTOM,1,1)
        grid.attach_next_to(__netEntry,netLabel, Gtk.PositionType.BOTTOM,1,1)
        grid.attach_next_to(analysisLabel,usrLabel, Gtk.PositionType.RIGHT,1,1)
        grid.attach_next_to(__analysisEntry,analysisLabel, Gtk.PositionType.BOTTOM,1,1)
        grid.attach_next_to(pwdLabel,netLabel, Gtk.PositionType.RIGHT,1,1)
        grid.attach_next_to(__pwdEntry,__netEntry, Gtk.PositionType.RIGHT,1,1)
        grid.attach_next_to(loginButton,__netEntry, Gtk.PositionType.BOTTOM,1,1)
        grid.attach_next_to(quitButton,loginButton, Gtk.PositionType.RIGHT,1,1)

    def on_loginButton_clicked(self,widget):
        
        send_msg(util.CommandMessage(content = 'set password "{msg}"'.format(msg = __pwdEntry.get_text())))
        #p_reaction = get_msg()
        send_msg(util.CommandMessage(content = 'set config SSH host  "{msg}"'.format(msg = __usrEntry.get_text())))
        #get_msg()
        send_msg(util.CommandMessage(content = 'set config SSH net  "{msg}"'.format(msg = __netEntry.get_text())))
        #get_msg()
        send_msg(util.CommandMessage(content = 'set config SSH analysis  "{msg}"'.format(msg = __analysisEntry.get_text())))
        #get_msg()
        send_msg(util.CommandMessage(content = 'save config'))
        #get_msg()
        
        #__parent.set_runButton_active()
        self.destroy()

    def on_quitButton_clicked(self,widget):
        #__parent.set_runButton_active()
        self.destroy()
        
    def on_xButton_clicked(self,widget,targetwidget):
        #__parent.set_runButton_active()
        self.destroy()
