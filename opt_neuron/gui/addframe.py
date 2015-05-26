#!/usr/bin/env python3
# coding: utf8

from gi.repository import Gtk

class AddFrame(Gtk.Window):
    def __init__(self,out_queue):
        Gtk.Window.__init__(self, title = "Algorithmusauswahl")

        self.chooseAlgo = Gtk.Box(spacing=6)
        self.add(self.chooseAlgo)

        #edit button
        self.editButton = Gtk.Button(label="Hinzufügen")
        self.editButton.connect("clicked", self.on_editButton_clicked)
        self.chooseAlgo.pack_start(self.editButton,True,True,0)        
        #quit button
        self.quitButton = Gtk.Button(label="Abbrechen")
        self.quitButton.connect("clicked", self.on_quitButton_clicked)
        self.chooseAlgo.pack_start(self.quitButton,True,True,0) 
        
        #scrollbar for choosing algorithm
        algoScrollbar = Gtk.Scrollbar(orientation = Gtk.Orientation.VERTICAL, adjustment = layout.get_vadjustment())
        grid.attach(algoScrollbar,1,1,0,0)

    def on_editButton_clicked(self,widget,out_queue):
        #TODO: send messages to queue, fill algo+params in table
        print("hinzugefügt")

    def on_quitButton_clicked(self,widget):
        #closes frame without saving anything
        self.destroy()
        
