#!/usr/bin/env python3
from . import addframe
from . import sshframe
from .. import util
from gi.repository import Gtk, Gdk
import logging
from .main import send_msg, get_msg, get_intercom_msg, flush_queues, abort_notify
from threading import Thread
#import numpy as np
import re
from time import sleep
import csv

logger = logging.getLogger(__name__)


class MainFrame(Gtk.Window):
    menu = Gtk.Menu()
    active_select = None

    def __init__(self):
        self.__running = True
        Gtk.Window.__init__(self, title="OPT Neuron Algorithmen Kommandant")
        self.connect("delete-event", self.close_call)


        self.set_border_width(10)
        self.set_default_size(1000, 600)

        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.hb.props.title = "OPT Algorithmen Kommandant"

        self.set_titlebar(self.hb)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 6)
        self.add(self.vbox)

        # +++ context menu +++

        self.abort = Gtk.MenuItem("abort")
        self.abort.connect("activate", self.on_abort)
        self.abort.set_sensitive(False)
        self.menu.append(self.abort)

        self.reset = Gtk.MenuItem("reset")
        self.reset.connect("activate", self.on_reset)
        self.reset.set_sensitive(False)
        self.menu.append(self.reset)

        self.menu.append(Gtk.SeparatorMenuItem())

        self.edit = Gtk.MenuItem("edit")
        self.edit.connect("activate", self.on_edit)
        self.edit.set_sensitive(False)
        self.menu.append(self.edit)

        self.rem = Gtk.MenuItem("remove")
        self.rem.connect("activate", self.on_remove)
        self.rem.set_sensitive(False)
        self.menu.append(self.rem)


        self.menu.show_all()


        # +++ TOP BAR THINGY +++
        self.tophbox = Gtk.Box(spacing = 6)
        self.vbox.pack_start(self.tophbox, False, True, 0)

        self.load_b = Gtk.Button(label = "load session")
        self.load_b.connect("clicked", self.load_session)
        self.tophbox.pack_start(self.load_b, False, True, 3)

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
        self.runstop.connect("clicked", self.on_run)
        #self.runstop.set_sensitive(False)
        self.bottomhbox.pack_start(self.runstop, False, True, 3)

        self.export = Gtk.Button(label = "Export Data")
        self.export.connect("clicked", self.on_export)
        self.bottomhbox.pack_end(self.export, False, True, 3)


    # +++ list store +++
        # (id, Alg_name, status, params)
        self.liststore = Gtk.ListStore(int, str, str, str)
     
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
        send_msg(util.MESSAGE_EXIT)
        flush_queues()
        Gtk.main_quit()

    def receive(self):
        # of a message comes along in here, it means a thread is ready.
        # if multithreading control is implemented, this needs to choose
        # the next thread in a list.
        
        while True:
            msg = get_intercom_msg()
            
            if str(msg.content) == "abort":
                return

            for i in self.running:
                if i[1] == msg.cmd_id:
                    try:
                        if msg.appendix.is_alive():
                            i[2] = msg.appendix
                            for alg in self.liststore:
                                if alg[0] == i[0]:
                                    alg[2] = "computing..."
                        else:
                            return
                    except:
                        for alg in self.liststore:
                            if alg[0] == i[0] and msg.content != "abort":
                                alg[2] = msg.content
                        
                        self.running.remove(i)

                        for alg in self.liststore:
                            if alg[2] == "stand-by":
                                self.initiate()
                                return
                            
                        self.cleanup()
                        return
            #return

    # this thread waits for incomming messages after a computation is started
    receive_t = None

    # this remembers the current running computation. If multithreading
    # is eventually implemented, this needs to hold a list of mapped
    # computational threads with list IDs.
    
    # index: alg in list,
   
    # running[i][0]: list id
    # running[i][1]: message id
    # running[i][2]: thread
    running = []

    def on_run(self, arg1):
        if len(self.liststore) == 0:
            return

        self.runstop.set_label("STOP")
        self.runstop.disconnect_by_func(self.on_run)
        self.runstop.connect("clicked", self.on_stop)

        self.load_b.set_sensitive(False)

        self.initiate()
        #print("Run initiated...")

    def initiate(self):
        for alg in self.liststore:
            if alg[2] == "stand-by":
                #print("preparing to run ID " + str(alg[0]) + "...")
                runstr = alg[3].replace(" ","")
                runstr = runstr.replace(","," ")
                p = re.compile('\w+=')
                runstr = p.sub('', runstr)

                c_message = util.CommandMessage(content = "start " + alg[1] + " " + runstr)
                self.running.append([alg[0], c_message.id, None])
                #                                           ^------- will be filled once thread is inbound
                send_msg(c_message, thread_intercom_id = c_message.id)
                self.receive_t = Thread(target = self.receive)
                self.receive_t.start()
                return

        self.cleanup()
        return

    def cleanup(self):
        self.runstop.set_label("Run")
        self.runstop.disconnect_by_func(self.on_stop)
        self.runstop.connect("clicked", self.on_run)

        self.load_b.set_sensitive(True)

        self.running = []

        flush_queues()
        return

    def on_stop(self, arg1):
        self.runstop.set_label("Run")
        self.runstop.disconnect_by_func(self.on_stop)
        self.runstop.connect("clicked", self.on_run)

        #print("Run aborted!")

        for alg in self.liststore:
            if alg[2] == "computing...":
                for i in self.running:
                    if i[0] == alg[0]:
                        #print("ABORT " + str(i[0]) + " " + str(i[1]) + ",")
                        send_msg(util.CommandMessage(content = "stop " + str(i[1])))
                        alg[2] = "aborted"
                        self.running.remove(i)

        if self.receive_t.is_alive():
            abort_notify(i[1])

        self.cleanup()

    def on_add(self, arg1):
        self.addbutton.set_sensitive(False)
        af = addframe.AddFrame(self)
        af.show_all()
        

    def on_edit(self, arg1):
        return



    # add alg to list
    def set_alg(self, alg):
        id = len(self.liststore) + 1

        # check if id is OK
        check = True
        while check:
            for x in self.liststore:
                if x[0] == id:
                    id = id+1
                    break
                else:
                    check = False
            check = False
        # granted, the above check isn't exactly pythonic, but I don' care...

        algname = alg[0]
        param_names = alg[1]
        param_values = alg[2]

        params_str = ""
        for i in range(0, len(param_values)):
            params_str = params_str + param_names[i+1] + "=" + param_values[i] + ", "

        params_str = params_str[:-2]

        
        self.liststore.append((id, algname, "stand-by", params_str))

    def set_addButton_active(self):
        self.addbutton.set_sensitive(True)


    def load_session(self, arg1):
        #name = askopenfilename()
        fc_d = Gtk.FileChooserDialog(title="Load Session",
                                     action=Gtk.FileChooserAction.OPEN,
                                     buttons=(Gtk.STOCK_CANCEL,
                                              Gtk.ResponseType.CANCEL,
                                              Gtk.STOCK_OPEN,
                                              Gtk.ResponseType.OK))
        res = fc_d.run()

        if res == Gtk.ResponseType.OK:
            with open(fc_d.get_filename(), 'r', newline='') as cf:
                csv_r = csv.reader(cf, delimiter=';', quotechar='"')
                
                self.liststore.clear()

                for r in csv_r:
                    self.liststore.append((int(r[0]), r[1], r[2], r[3]))

                cf.close()


        fc_d.destroy()

    def on_export(self, arg1):
        #name = askopenfilename()
        fc_d = Gtk.FileChooserDialog(title="Export Session",
                                     action=Gtk.FileChooserAction.SAVE,
                                     buttons=(Gtk.STOCK_CANCEL,
                                              Gtk.ResponseType.CANCEL,
                                              Gtk.STOCK_SAVE,
                                              Gtk.ResponseType.OK))
        res = fc_d.run()

        if res == Gtk.ResponseType.OK:
            with open(fc_d.get_filename(), 'w', newline='') as cf:
                csv_w = csv.writer(cf, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                for i in self.liststore:
                    csv_w.writerow(i[:])

                cf.close()


        fc_d.destroy()

        return

    def close_call(self, arg1, arg2):
        #self.cleanup()
        self.destroy()
        self.__on_destroy()
        #Gtk.main_quit()
        
        return True


    def on_abort(self, arg1):
        # selection set at this point
        iter = self.liststore.get_iter(self.active_select)
        r_id = self.liststore.get_value(iter, 0)
        
        for i in self.running:
            if i[0] == r_id:
                print("ABORT " + str(i[0]) + " " + str(i[1]) + ";")
                send_msg(util.CommandMessage(content = "stop " + str(i[1])))
                self.liststore.set_value(iter, 2, "aborted")

                self.running.remove(i)

                if self.receive_t.is_alive():
                    abort_notify(i[1])
                # check if we're in perpetual mode:
                if self.runstop.get_label() == "STOP":
                    self.initiate()

        return

    def on_reset(self, arg1):
        return

    def on_edit(self, arg1):
        return

    def on_remove(self, arg1):
        # selection set at this point
        iter = self.liststore.get_iter(self.active_select)
        self.liststore.remove(iter)
        return

    def __sanitize_ctx_menu():
        return

    def on_rightclick(self, tv, event):
        if event.button == 3 and event.type == Gdk.EventType.BUTTON_PRESS:
            (tp, tvc, c_y, c_x) = tv.get_path_at_pos(event.x, event.y)

            self.abort.set_sensitive(False)
            self.rem.set_sensitive(False)

            # +++ ACTIVE SELECTION SET +++
            self.active_select = tp
            
            iter = self.liststore.get_iter(tp)
            if self.liststore.get_value(iter, 2) == "computing...":
                self.abort.set_sensitive(True)
            else:
                self.rem.set_sensitive(True)

            self.menu.popup(None, None, None, None, 0, Gtk.get_current_event_time())

