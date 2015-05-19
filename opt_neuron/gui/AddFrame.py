
class AddFrame(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title = "Algorithmusauswahl")

        self.chooseAlgo = Gtk.Box(spacing=6)
        self.add(self.chooseAlgo)

        #edit button
        self.editButton = Gtk.Button(label="Hinzufügen")
        self.editButton.connect("clicked", self.on_editButton_clicked)
        self.chooseAlgo.pack_start(self.editButton,True,True,0)        

        self.quitButton = Gtk.Button(label="Abbrechen")
        self.quitButton.connect("clicked", self.on_quitButton_clicked)
        self.chooseAlgo.pack_start(self.quitButton,True,True,0) 

    def on_editButton_clicked(self,widget):
        #TODO: send messages to queue, fill algo+params in table
        print("hinzugefügt")

    def on_quitButton_clicked(self,widget):
        #closes frame without saving anything
        self.destroy()
        
