# coding: utf8

#TODO:  
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
__labelBox = None
__i_length = None

class AddFrame(Gtk.Window):
    def __init__(self,parent):
        Gtk.Window.__init__(self, title = "Algorithm selection")

        global __hbox
        global __paramBox
        global __labelBox
        global __algoCombo
        global __algos
        global __argSpecs
        global __algoList
        global __algo
        global __parent
        global __i_length
        
        self.set_default_size(100,100)
        self.set_border_width(10)
        self.set_resizable(0)
        self.connect("delete-event", self.on_destroy)
        
        Header = Gtk.HeaderBar(title = "Algorithm selection")
        
        # define (global) variables
        __hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 6)
        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)
        
        __paramBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)
        __labelBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)
        
        __algos = []
        __argSpecs = []
        __algo = ""      
        __parent = parent

        #edit button
        editButton = Gtk.Button(label="adopt")
        editButton.connect("clicked", self.on_editButton_clicked)  

        #quit button
        quitButton = Gtk.Button(label="quit")
        quitButton.connect("clicked", self.on_quitButton_clicked)
        
        # pack together buttons
        buttonBox = Gtk.ButtonBox()
        buttonBox.pack_end(editButton, False,False,0)
        buttonBox.pack_end(quitButton, False,False,0)
        vbox.pack_end(buttonBox,False,False,0)
        
        # arrange frame
        __algoCombo = Gtk.ComboBoxText()
        __algoCombo.connect("changed", self.on_algo_combo_changed)
        vbox.pack_start(__algoCombo,False,False,0)      
        
        __hbox.pack_start(vbox,False,False,0)
        __hbox.pack_end(__labelBox,False,False,0)
        __hbox.pack_end(__paramBox,False,False,0)
        
        self.fillAlgoStore()
        __algoCombo.set_active(0)
        self.add(__hbox)

    def on_editButton_clicked(self,widget):
    # Function that calls the function "set_alg" from mainframe with arguments in form
    # of [algorithm name [argument name 1,...,argument name n] [argument 1,...,argument n]],
    # where argument is the value, which the user defined for its corresponding algorithm name.
        global __algo
        global __paramBox
        global __parent
        global __i_length
        
        for i in __paramBox:
            try:
                inputNum = int(str(i.get_text()))
                if i == __i_length:
                    if inputNum not in range(1,1000000):
                        alert = Alert(self)
                        response = alert.run()
                        return
            except ValueError: 
                alert = StrAlert(self)
                response = alert.run()
                return
                
        args = __argSpecs[(__algos.index(__algo))].args
        specName = [(i) for i in args] 
        spec = [(j.get_text()) for j in __paramBox]
        __parent.set_alg([__algo, specName, spec])
        __parent.set_addButton_active()
        self.destroy()

    def on_quitButton_clicked(self,widget):
    # Function that closes the frame without saving anything
        global __parent
        __parent.set_addButton_active()
        self.destroy()
        
    def on_algo_combo_changed(self,widget):
    # Function that edits the whole frame, so that a chosen algorithm from the ComboBox
    # gets its proper parameter by number, name and default values.
        global __paramBox
        global __labelBox
        global __algos
        global __argSpecs
        global __hbox
        global __algo
        global __i_length
        # clear label and param boxes
        __hbox.remove(__paramBox)  
        __hbox.remove(__labelBox)
        # rebuild/clear label and params
        __paramBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)
        __labelBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)
        # get the clicked algorithm and its parameter
        algo_iter = widget.get_active_iter()
        if algo_iter != None:
            model = widget.get_model()
            __algo = model[algo_iter][0]
            args = __argSpecs[(__algos.index(__algo))].args
        # build labels and entries and pack them to their boxes
        for i in range(1,len(args)):
            param = Gtk.Entry()
            if i == 1:
                param.set_text("num of param to optimize")
                __i_length = param
            elif  __argSpecs[__algos.index(__algo)].defaults == None:
                param.set_text(str(0))
            else:
                print(str(i))
                param.set_text(str(__argSpecs[__algos.index(__algo)].defaults[i-2]))
            
            label = Gtk.Label(args[i])
            
            __labelBox.pack_start(label,True,True,0)
            __paramBox.pack_start(param,True,True,0)
            
        __hbox.pack_end(__paramBox,False,False,0)
        __hbox.pack_end(__labelBox,False,False,0)
        # show differences
        self.show_all()

    def fillAlgoStore(self):
    # Asks algorithms from the core and fills the ComboBox with those algorithms,
    # so that the user can choose from the algorithms which are defined in the 
    # config.
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
        
        for x in range(num_algos): 
            __algos.append(names[x])
            __argSpecs.append(argSpecs[x])
            __algoCombo.append_text(names[x])


    def set_algo_from_main(algo, values):
    # Function that is calles from mainframe when user wants to reedit an algorithm he already chose.
    # The ComboBox is set to the algorithm to edit and the default values are overwritten with the
    # already edited ones.
        global __algoCombo
        global __algos
        global __paramBox
        
        __algoCombo.set_active(__algos.index(algo))
        
        i = 0
        for j in __paramBox:
            j.set_text(str(i))
            i = i+1
        
    def on_destroy(self, bla, blubb):
        global __parent
        __parent.set_addButton_active()
        self.destroy()
        
class Alert(Gtk.Dialog):
    def __init__(self,parent):
        Gtk.Dialog.__init__(self,"ValueError",parent,0)
            
        self.set_default_size(150,50)
        
        label = Gtk.Label("The parameter 'i_length' has to be in range of 1 to 1000000." )

        box = self.get_content_area()
        box.add(label)
        self.show_all()
     
class StrAlert(Gtk.Dialog):
    def __init__(self,parent):
        Gtk.Dialog.__init__(self,"ValueError",parent,0)
            
        self.set_default_size(150,50)
        
        label = Gtk.Label("The parameters have to be numbers.")

        box = self.get_content_area()
        box.add(label)
        self.show_all
