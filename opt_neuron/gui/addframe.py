#!/usr/bin/env python3
# coding: utf8

from gi.repository import Gtk

class AddFrame(Gtk.Window):
    def __init__(self,out_queue):
        Gtk.Window.__init__(self, title = "Algorithmusauswahl")
	
	self.out_queue = out_queue
	
	#horizontal box for buttons 
        self.buttonRow = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing=6)
        self.add(self.buttonRow)

        #edit button
        self.editButton = Gtk.Button(label="Hinzufügen")
        self.editButton.connect("clicked", self.on_editButton_clicked)
        self.buttonRow.pack_start(self.editButton,True,True,0)        
        #quit button
        self.quitButton = Gtk.Button(label="Abbrechen")
        self.quitButton.connect("clicked", self.on_quitButton_clicked)
        self.buttonRow.pack_start(self.quitButton,True,True,0) 
        
	#horizontal box for algo/params
	self.paramBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 6)

        #scrollbar with algorithms from config
	#TODO: import algorithms from config, read in
        self.algoScrollbar = Gtk.Scrollbar(orientation = Gtk.Orientation.VERTICAL, adjustment = layout.get_vadjustment())
	self.paramBox.pack_start(self.algoScrollbar, True, True, 0)
	self.scrollbarLabel = Gtk.Label()
	self.scrollbarLabel.set_text("Auszuführender Algorithmus")

	#box for wished parameters
	self.chooseParams = Gtk.Box(spacing = 6)
	self.paramBox.pack_start(self.chooseParams, True, True, 0)

	#Entries for parameters
	#TODO: Parameter spezifisch für jeden möglichen Algo?!
	self.param1 = Gtk.Entry()
	self.param1.set_text("param1")
	chooseParams.pack_start(self.param1, True, True, 0)

	self.param2 = Gtk.Entry()
	self.param2.set_text("param2")
	chooseParams.pack_start(self.param2, True, True, 0)

	self.param3 = Gtk.Entry()
	self.param3.set_text("param3")
	chooseParams.pack_start(self.param3, True, True, 0)

	self.param4 = Gtk.Entry()
	self.param4.set_text("param4")
	chooseParams.pack_start(self.param4, True, True, 0)

    def on_editButton_clicked(self,widget,out_queue):
        #TODO: send messages to queue, fill algo+params in table
        print("hinzugefügt")

    def on_quitButton_clicked(self,widget):
        #closes frame without saving anything
	self.connect("delete_event",self.close_call)
        self.destroy()
	
        