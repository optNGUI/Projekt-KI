# coding: utf8

import logging
from .main import send_msg, get_msg
from .. import util
from gi.repository import Gtk

__algoBox = None
__algoCombo = None
__algoStore = None
__algoList = None

class AddFrame(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title = "Algorithmusauswahl")
        
        self.set_default_size(300,200)
        self.set_border_width(10)
        
        Header = Gtk.HeaderBar(title = "Algorithmusauswahl")
        
        hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 6)
        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)

        global __algoBox
        global __algoCombo
        global __algoStore
        global __algoList
        
        __algoBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)

        #edit button
        editButton = Gtk.Button(label="Übernehmen")
        editButton.connect("clicked", self.on_editButton_clicked)  
        
        #quit button
        quitButton = Gtk.Button(label="Abbrechen")
        quitButton.connect("clicked", self.on_quitButton_clicked)
        
        buttonBox = Gtk.ButtonBox()
        buttonBox.pack_end(editButton, False,False,0)
        buttonBox.pack_end(quitButton, False,False,0)
        vbox.pack_end(buttonBox,False,False,0)

        __algoStore = Gtk.ListStore(str, object)  #,str)

        __algoCombo = Gtk.ComboBoxText()  #.new_with_model(__algoStore)
        __algoCombo.connect("changed", self.on_algo_combo_changed)
        vbox.pack_start(__algoCombo,False,False,0)      
        
        self.fillAlgoStore()
        #Entries for parameters
        #TODO: Parameter spezifisch für jeden möglichen Algo?!
        
        # param1 = Gtk.Entry()
        # param1.set_text("param1")
        # vbox.pack_start(param1,False,False,0)

        # param2 = Gtk.Entry()
        # param2.set_text("param2")
        # vbox.pack_start(param2,False,False,0)
        
        # param3 = Gtk.Entry()
        # param3.set_text("param3")
        # vbox.pack_start(param3,False,False,0)
        
        # param4 = Gtk.Entry()
        # param4.set_text("param4")
        # vbox.pack_start(param4,False,False,0)
        
        hbox.pack_start(vbox,False,False,0)
        hbox.pack_end(__algoBox,False,False,0)
        self.add(hbox)

    def on_editButton_clicked(self,widget):
        #TODO: fill algo+params in table in mainframe

        #set_alg(__alg+param)
        set_addButton_active()
        print("hinzugefügt")
        #self.destroy()

    def on_quitButton_clicked(self,widget):
        #closes frame without saving anything
        set_addButton_active()
        self.destroy()
        
    def on_algo_combo_changed(self,widget):
        algo_iter = widget.get_active_iter()
 
        if algo_iter != None:
            model = widget.get_model()
            algo = model[algo_iter][0]
            self.build_param_entries(model[algo_iter])
        
            
    def build_param_entries(self,algo):
        global __algoBox
        global __algoStore

        for i in range(1,len(__algoStore.get_iter(algo))):
            param[i] = Gtk.Entry()
            param[i].set_text(algo[i])
            __algoBox.pack_start(param(i),False,False,0)

    def fillAlgoStore(self):
        #asks algorithms from core and fills the combobox
        global __algoCombo
        global __algoStore
        global __algoList

        send_msg(util.CommandMessage(content = "get algorithms"))
        __algoList = get_msg()
       
        appendix = __algoList.appendix
        num_algos = len(appendix)
        
        names = appendix[0]
        function = appendix[1]
        argSpecs = appendix[2]

        #print("appendix = ",appendix)

        for x in range(num_algos-1): 
            __algoStore.append([names[x],argSpecs[x]])  #,function[x]])
            __algoCombo.append_text(names[x])

    def set_algo_from_main():
        # voreinstellung von algo nachdem editbutton in main gedrückt
        print('editButton erkannt, Voreinstellung vorgenommen.')
        
