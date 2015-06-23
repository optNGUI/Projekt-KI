# coding: utf8

import logging
from .main import send_msg, get_msg
from .. import util
from gi.repository import Gtk

__algoBox = None

class AddFrame(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title = "Algorithmusauswahl")
        
        self.set_default_size(300,200)
        self.set_border_width(10)
        
        Header = Gtk.HeaderBar(title = "Algorithmusauswahl")
        
        hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 6)
        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)

        global __algoBox
        __algoBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)

        #edit button
        editButton = Gtk.Button(label="Hinzufügen")
        editButton.connect("clicked", self.on_editButton_clicked)  
        
        #quit button
        quitButton = Gtk.Button(label="Abbrechen")
        quitButton.connect("clicked", self.on_quitButton_clicked)
        
        buttonBox = Gtk.ButtonBox()
        buttonBox.pack_end(editButton, False,False,0)
        buttonBox.pack_end(quitButton, False,False,0)
        vbox.pack_end(buttonBox,False,False,0)
        
        algoStore = Gtk.ListStore(str)
        #self.fillAlgoStore()
        algo_combo = Gtk.ComboBox.new_with_model(algoStore)
        algo_combo.connect("changed", self.on_algo_combo_changed)
        vbox.pack_start(algo_combo,False,False,0)
        
        #Entries for parameters
        #TODO: Parameter spezifisch für jeden möglichen Algo?!
        
        param1 = Gtk.Entry()
        param1.set_text("param1")
        vbox.pack_start(param1,False,False,0)

        param2 = Gtk.Entry()
        param2.set_text("param2")
        vbox.pack_start(param2,False,False,0)
        
        param3 = Gtk.Entry()
        param3.set_text("param3")
        vbox.pack_start(param3,False,False,0)
        
        param4 = Gtk.Entry()
        param4.set_text("param4")
        vbox.pack_start(param4,False,False,0)
        
        hbox.pack_start(vbox,False,False,0)
        hbox.pack_end(__algoBox,False,False,0)
        self.add(hbox)
        
    def on_editButton_clicked(self,widget):
        #TODO: fill algo+params in table in mainframe
        #return [...,param1.get_text(),param2.get_text(),param3.get_text(),param4.get_text()]
        print("hinzugefügt")
        #self.destroy()

    def on_quitButton_clicked(self,widget):
        #closes frame without saving anything
        self.destroy()
        
    def on_algo_combo_changed(self,widget):
        algo_iter = widget.get_active_iter()
        if algo_iter != None:
            model = widget.get_model()
            algo = model[algo_iter][0]
            self.build_param_entries(model[algo_iter])
        print("selected algorithm: %s" %algo)
        
    def fillAlgoStore(self,widget):
        #asks algorithms from core and fills the combobox
        send_msg(util.CommandMessage(content = 'get algorithms'))
        algoList = None
        received = 0
    
        while received == 0:
            algoList = get_msg()
            if algoList != None:
                received = 1
 
        for x in algoList:
            algoStore.append(x)#[0])

    def build_param_entries(self,algo):
        for i in range(1,len(algo)):
            param[i] = Gtk.Entry()
            param[i].set_text(algo[i])
            __algoBox.pack_start(param(i),False,False,0)
