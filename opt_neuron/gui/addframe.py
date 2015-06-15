#!/usr/bin/env python3
# coding: utf8

from gi.repository import Gtk


class AddFrame(Gtk.Window):
    def __init__(self,in_queue,out_queue):
        Gtk.Window.__init__(self, title = "Algorithmusauswahl")
        self.in_queue = in_queue
        self.out_queue = out_queue
	
        self.set_default_size(300,200)
        self.set_border_width(10)
        
        Header = Gtk.HeaderBar(title = "Algorithmusauswahl")
        
        #vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)
        #vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)
        grid = Gtk.Grid()
        self.add(grid)

        #edit button
        editButton = Gtk.Button(label="Hinzufügen")
        editButton.connect("clicked", self.on_editButton_clicked)  
        
        #quit button
        quitButton = Gtk.Button(label="Abbrechen")
        quitButton.connect("clicked", self.on_quitButton_clicked)
        
        grid.add(editButton)
        grid.add(quitButton)
        #vbox.pack_end(editButton, True,True,0)
        #vbox.pack_end(quitButton, True,True,0)
        
        #horizontal box for algo/params
        paramBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 6)

        #scrolled Window with algorithms from config
        #TODO: import algorithms from config, read in
        #algoScrollWin = Gtk.ScrolledWindow(None,None)
        #algoScrollWin.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        #grid.add(algoScrollWin)
        
        algoStore = Gtk.ListStore(str)
        #self.fillAlgoStore()
        algo_combo = Gtk.ComboBox.new_with_model(algoStore)
        algo_combo.connect("changed", self.on_algo_combo_changed)
        #vbox.pack_start(algo_combo,False,False,0)
        
        
        #scrollWinLabel = Gtk.Label()
        #scrollWinLabel.set_text("Auszuführender Algorithmus")

        #Entries for parameters
        #TODO: Parameter spezifisch für jeden möglichen Algo?!
        param1 = Gtk.Entry()
        param1.set_text("param1")
        #vbox.pack_start(param1,False,False,0)

        param2 = Gtk.Entry()
        param2.set_text("param2")
        #vbox.pack_start(param2,False,False,0)
        
        param3 = Gtk.Entry()
        param3.set_text("param3")
        #vbox.pack_start(param3,False,False,0)
        
        param4 = Gtk.Entry()
        param4.set_text("param4")
        #vbox.pack_start(param4,False,False,0)
        
        #grid.attach(algoCombo, 1,0,2,1)
        grid.attach(algo_combo,0,0,0,0)
        grid.attach(param1,1,1,1,1)
        grid.attach_next_to(param2,param1, Gtk.PositionType.RIGHT,1,1)
        grid.attach_next_to(param3,param1, Gtk.PositionType.BOTTOM,1,1)
        grid.attach_next_to(param4,param2, Gtk.PositionType.BOTTOM,1,1)
        grid.attach(editButton,2,3,4,4)
        grid.attach_next_to(quitButton,editButton, Gtk.PositionType.RIGHT,1,1)
        #self.add(vbox)
        #self.add(paramBox)
        #self.show_all()
        
    def on_editButton_clicked(self,widget,in_queue):
        #TODO: send messages to queue, fill algo+params in table
        self.out_queue.put(util.StatusMessage(content = "choosed algorithm: %s" %algorithm))
        print("hinzugefügt")

    def on_quitButton_clicked(self,widget):
        #closes frame without saving anything
        #self.connect("delete_event",self.close_call)
        self.destroy()
        
    def on_algo_combo_changed(self,widget):
        print("algorithm changed")
    #def fillAlgoStore(self):
        #asks algorithms from core and fills the combobox
        #self.out_queue.put(CommandMessage(get config [Algorithm])
        #try
            #self.in_queue.get(RetValMessage)
        
        #for x in in_queue:
            #algoStore.append(x)
            
