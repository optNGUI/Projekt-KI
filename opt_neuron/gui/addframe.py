# coding: utf8

#TODO:  gray out edit button, when nothing is choosed,
#	set default values in param,
#	set first row to be there from beginning
#	on x clicked, do parent.set_addButton_active()
#	same at sshFrame
import logging
from .main import send_msg, get_msg
from .. import util
from gi.repository import Gtk

__hbox = None
__paramBox = None
__algoCombo = None
__algos = None
__argSpecs = None
__algoList = None
__algo = None
__parent = None

class AddFrame(Gtk.Window):
    def __init__(self,parent):
        Gtk.Window.__init__(self, title = "Algorithmusauswahl")
        print("..."+str(self))
        global __hbox
        global __paramBox
        global __algoCombo
        global __algos
        global __argSpecs
        global __algoList
        global __algo
        global __parent
        
        self.set_default_size(200,200)
        self.set_border_width(10)
        
        Header = Gtk.HeaderBar(title = "Algorithmusauswahl")
        
        __hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 6)
        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)
        __paramBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)

        __algos = []
        __argSpecs = []
        __algo = ""      
        __parent = parent

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

        __algoCombo = Gtk.ComboBoxText()
        __algoCombo.connect("changed", self.on_algo_combo_changed)
        vbox.pack_start(__algoCombo,False,False,0)      
        
        self.fillAlgoStore()
        
        __hbox.pack_start(vbox,False,False,0)
        __hbox.pack_end(__paramBox,False,False,0)
        self.add(__hbox)

    def on_editButton_clicked(self,widget):
        # Function that calls the function "set_alg" from mainframe with arguments in form
        # of [ algorithm name, argument name 1,...,argument name n, argument 1, argument n],
        # where argument is the value, which the user defined for the corresponding algorithm name.
        global __algo
        global __paramBox
        global __parent

        args = __argSpecs[(__algos.index(__algo))].args
        specName = [(i) for i in args] 
        spec = [(j.get_text()) for j in __paramBox]
        
        __parent.set_alg([__algo, spec])
        __parent.set_addButton_active()
        self.destroy()

    def on_quitButton_clicked(self,widget):
        #closes frame without saving anything
        global __parent
        __parent.set_addButton_active()
        self.destroy()
        
    def on_algo_combo_changed(self,widget):
        global __paramBox
        global __algos
        global __argSpecs
        global __hbox
        global __algo

        __hbox.remove(__paramBox)  
        __paramBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)
        algo_iter = widget.get_active_iter()

        if algo_iter != None:
            model = widget.get_model()
            __algo = model[algo_iter][0]
            args = __argSpecs[(__algos.index(__algo))].args
            print("args: "+str(args))
        
        for i in range(1,len(args)):
            param = Gtk.Entry()
            param.set_text(args[i])
            __paramBox.pack_start(param,False,False,0)
        
        __hbox.pack_end(__paramBox,False,False,0)
        self.show_all()

    def fillAlgoStore(self):
        #asks algorithms from core and fills the combobox
        global __algoCombo
        global __algos
        global __argSpecs
        global __algoList

        send_msg(util.CommandMessage(content = "get algorithms"))
        __algoList = get_msg()
       
        appendix = __algoList.appendix
        num_algos = len(appendix)
        
        names = appendix[0]
        function = appendix[1]
        argSpecs = appendix[2]

        for x in range(num_algos-1): 
            __algos.append(names[x])
            __argSpecs.append(argSpecs[x])
            __algoCombo.append_text(names[x])

    def set_algo_from_main(algo):

        # voreinstellung von algo nachdem editbutton in main gedrückt
        print('editButton erkannt, Voreinstellung vorgenommen.')
        
