#!/usr/bin/env python3
from . import addframe
from . import sshframe
from .. import util
from gi.repository import Gtk, Gdk
import logging
from .main import send_msg, get_msg
from threading import Thread
import numpy as np

logger = logging.getLogger(__name__)


class MainFrame(Gtk.Window):
    menu = Gtk.Menu()
    active_select = None

    def __init__(self, in_queue, out_queue):
        self.__running = True
        Gtk.Window.__init__(self, title="OPT Neuron Algorithmen Kommandant")
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.connect("delete-event", self.close_call)


        self.set_border_width(10)
        self.set_default_size(500, 450)

        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.hb.props.title = "OPT Algorithmen Kommandant"

        self.set_titlebar(self.hb)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 6)
        self.add(self.vbox)

        # +++ context menu +++

        self.rem = Gtk.MenuItem("remove")
        self.rem.connect("activate", self.on_remove)
        self.rem.set_sensitive(False)
        self.menu.append(self.rem)
        self.abort = Gtk.MenuItem("abort")
        self.abort.connect("activate", self.on_abort)
        self.abort.set_sensitive(False)
        self.menu.append(self.abort)
        self.menu.show_all()


        # +++ TOP BAR THINGY +++
        self.tophbox = Gtk.Box(spacing = 6)
        self.vbox.pack_start(self.tophbox, False, True, 0)

        self.label_one = Gtk.Label("Session:")
        self.tophbox.pack_start(self.label_one, False, True, 3)

        self.search = Gtk.Button(label = "load config")
        self.search.connect("clicked", self.load_file)
        self.tophbox.pack_start(self.search, False, True, 3)

        self.addbutton = Gtk.Button(label = "add algorithm")
        self.addbutton.connect("clicked", self.on_add)
        self.tophbox.pack_end(self.addbutton, False, True, 3)

    # +++ scroll pane +++
        self.scrollspace = Gtk.ScrolledWindow()
        #self.scrollspace.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.scrollspace.set_vexpand(True)
        self.scrollspace.set_hexpand(True)

        self.vbox.pack_start(self.scrollspace, True, True, 3)

    # +++ EDIT BUTTONS +++

    #    self.optionhbox = Gtk.Box(spacing = 6)
    #    self.vbox.pack_start(self.optionhbox, False, True, 0)

    #    self.editbutton = Gtk.Button(label = "edit", name = "EditButton")
    #    self.editbutton.connect("clicked", self.on_edit)
        # self.editbutton.set_sensitive(False)
    #    self.optionhbox.pack_end(self.editbutton, False, True, 3)

    #    self.removebutton = Gtk.Button(label = "remove", name = "RemoveButton")
    #    self.editbutton.connect("clicked", self.on_remove)
        # self.editbutton.set_sensitive(False)


    # +++ BOTTOM BAR THINGY +++
        self.bottomhbox = Gtk.Box(spacing = 6)
        self.vbox.pack_start(self.bottomhbox, False, True, 0)

    #    self.label_one = Gtk.Label("wtf..?")
    #    self.tophbox.pack_start(self.label_one, False, True, 3)

        self.runstop = Gtk.Button(label = "Run", name = "RunStop")
        self.runstop.connect("clicked", self.on_runstop)
        #self.runstop.set_sensitive(False)
        self.bottomhbox.pack_start(self.runstop, False, True, 3)

        self.export = Gtk.Button(label = "Export Data")
        #self.export.connect("clicked", self.on_add)
        self.bottomhbox.pack_end(self.export, False, True, 3)


    # +++ list store +++
        # (id, Alg_name, status, params)
        self.liststore = Gtk.ListStore(int, str, str, str)
        #self.liststore.append((1, "smart algo1", "stand_by", "params"))
        #self.liststore.append((2, "smart algo2", "stand_by", "params"))
        #self.liststore.append((3, "smart algo3", "stand_by", "params"))
        #self.liststore.append((4, "smart algo4", "stand_by", "params"))
        #self.liststore.append((5, "smart algo5", "stand_by", "params"))
  
    # +++ view +++
        self.tree = Gtk.TreeView(self.liststore)
        self.tree.set_grid_lines(Gtk.TreeViewGridLines.HORIZONTAL)

        self.renderer = Gtk.CellRendererText()
        self.column = Gtk.TreeViewColumn("ID", self.renderer, text=0)
        self.column.set_resizable(True)
        self.column.set_min_width(20)
        self.tree.append_column(self.column)

        self.renderer = Gtk.CellRendererText()
        self.column = Gtk.TreeViewColumn("Algorithm", self.renderer, text=1)
        self.column.set_resizable(True)
        self.column.set_min_width(20)
        self.tree.append_column(self.column)

        self.renderer = Gtk.CellRendererText()
        self.column = Gtk.TreeViewColumn("Status", self.renderer, text=2)
        self.column.set_resizable(True)
        self.column.set_min_width(20)
        self.tree.append_column(self.column)
        
        self.renderer = Gtk.CellRendererText()
        self.column = Gtk.TreeViewColumn("Parameters", self.renderer, text=3)
        self.column.set_resizable(True)
        self.column.set_min_width(20)
        self.tree.append_column(self.column)

        # connect right mouse button thing
        self.treeselect = self.tree.get_selection()
        self.tree.connect("button_press_event", self.on_rightclick)

        # +++ put tree view into scrollable pane
        self.scrollspace.add(self.tree)

        style_provider = Gtk.CssProvider()

        css = """
            #RunStop             { background: #d56a00; font-weight: bold; color: #202020}
            #RunStop:hover       { background: shade(#d56a00, 1.2); }
            #RunStop:insensitive { background: shade(#d56a00, 0.8); }
            #RunStop:active      { background: shade(#d56a00, 2.0); }
        """

        style_provider.load_from_data(bytes(css.encode()))
 
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), style_provider,
                                                 Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # self.receiver_t = Thread( target=self.receive )
        # self.receiver_t.start()
        self.show_all()

    def __on_destroy(self):
        print("closing Gui!")
        self.__running = False
        Thread( target=self.sendit, args=(util.MESSAGE_EXIT,) ).start()
        Gtk.main_quit()
        print("asd")

    # def receive(self):
        # print("thread started")
        # while self.__running:
            # print("waiting...")
            # msg = self.in_queue.get()
            # print("message received!")
            # print(msg)

            # alert = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, msg)
            # alert.connect("delete-event", alert.destroy)
            # alert.run()
            # print("msg box closed")
            # alert.destroy()
        
        # print("closed?")

    def sendit(self, message):
        print(self)
        print(message)
        send_msg(message)
        #send_msg(message)

    def on_runstop(self, arg1):
        self.runstop.set_label("STOP")
        print("runstop")

    def on_add(self, arg1):
        print("Addwin opens...")
        #self.liststore.append((30, "testinput", "status", "params"))
        #send_msg(util.MESSAGE_EXIT)
        self.addbutton.set_sensitive(False)

        af = addframe.AddFrame(self)
        #self.t = Thread( target=self.sendit, args=(util.CommandMessage(content="echo SHIT"),) )
        #self.t.start()
        af.show_all()

    def on_edit(self, arg1):
        return

    # add alg to list
    def set_alg(self, alg):
        id = len(self.liststore) + 1

        # check if id is OK
        for i in range(id-1, len(self.liststore)):
            print(self.liststore.get_value(i, 0))

        algname = alg[0]
        param_names = alg[1]
        param_values = alg[2]

        print(algname)
        print(alg)

        params_str = ""
        for i in range(0, len(param_values)):
            params_str = params_str + param_names[i+2] + "=" + param_values[i] + "; "

        params_str = params_str[:-2]

        
        self.liststore.append((id, algname, "stand-by", params_str))

        print("set alg")

    def set_addButton_active(self):
        self.addbutton.set_sensitive(True)


    def load_file(self):
        fname = askopenfilename()

        if fname:
            try:
                print("""self.settings["template"].set(fname)""")
            except:
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
            return

    def add_task_f(self):
        self.add_task.config(state=DISABLED)
        self.addwin = Toplevel()
        self.addwin.wm_protocol("WM_DELETE_WINDOW", lambda:self.addwin_cancel())
        self.addwin.okay = Button(self.addwin, text="OK", command=self.addwin_ok, width=2, height=2)
        self.addwin.okay.grid(row=1, column=1)
        self.addwin.cancel = Button(self.addwin, text="Cancel", command=self.addwin_cancel, width=2, height=2)
        self.addwin.cancel.grid(row=1, column=2)


    def addwin_ok(self):
        # daten in scheduler hinzufugen
        self.add_task.config(state=NORMAL)
        self.addwin.destroy()

    def addwin_cancel(self):
        if messagebox.askokcancel("Quit", "Close without change?"):
            self.add_task.config(state=NORMAL)
            self.addwin.destroy()

    def close_call(self, arg1, arg2):
        # TODO check ob noch was laeuft, etc...
        #self.out_queue.put(util.StatusMessage(content = "in OH MEIN GOTT WAS IST GESCHEHEN!?"))
        #self.out_queue.put(util.MESSAGE_EXIT)
        print("end")
        self.destroy()
        self.__on_destroy()
        #Gtk.main_quit()
        
        return True

    def on_remove(self, arg1):
        print("REMOVE SIGNAL GET")
        return

    def on_abort(self, arg1):
        print("ABORT SIGNAL GET")
        return


    def on_rightclick(self, tv, event):
        if event.button == 3 and event.type == Gdk.EventType.BUTTON_PRESS:
            (tp, tvc, c_y, c_x) = tv.get_path_at_pos(event.x, event.y)

            self.abort.set_sensitive(False)
            self.rem.set_sensitive(False)

            # +++ ACTIVE SELECTION SET +++
            self.active_select = tp
            print("Treepath: " + str(self.active_select.to_string()))
            
            #print(self.liststore.get_value(self.active_select, 0))
            iter = self.liststore.get_iter(tp)
            if self.liststore.get_value(iter, 2) == "computing...":
                self.abort.set_sensitive(True)
            else:
                self.rem.set_sensitive(True)

            #print(self.liststore.get_value(iter, 2))

            self.menu.popup(None, None, None, None, 0, Gtk.get_current_event_time())




    def show_menu(self, *args):
        i1 = Gtk.MenuItem("Item 1")
        menu.append(i1)
        i2 = Gtk.MenuItem("Item 2")
        menu.append(i2)
        menu.show_all()
        menu.popup(None, None, None, None, 0, Gtk.get_current_event_time())
        print("Done")

