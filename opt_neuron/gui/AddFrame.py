from gi.repository import Gtk

class AddFrame(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title = "choose your Algorithm")

        self.choose_Algo = Gtk.Box(spacing=6)
        self.add(self.choose_Algo)
        print("nix")
