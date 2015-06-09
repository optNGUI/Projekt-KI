#!/usr/bin/env python3
from . import addframe
from .. import util
from gi.repository import Gtk

class MainFrame(Gtk.Window):
    def __init__(self, in_queue, out_queue):
        Gtk.Window.__init__(self, title="GtkWin")
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

    # +++ TOP BAR THINGY +++
        self.tophbox = Gtk.Box(spacing = 6)
        self.vbox.pack_start(self.tophbox, False, True, 0)

        self.label_one = Gtk.Label("something...")
        self.tophbox.pack_start(self.label_one, False, True, 3)

        self.search = Gtk.Button(label = "...")
        self.search.connect("clicked", self.load_file)
        self.tophbox.pack_start(self.search, False, True, 3)

        self.addbutton = Gtk.Button(label = "add")
        self.addbutton.connect("clicked", self.on_add)
        self.tophbox.pack_end(self.addbutton, False, True, 3)


        self.scrollspace = Gtk.ScrolledWindow()
        self.scrollspace.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.scrollspace.set_vexpand(True)

        #self.

        self.vbox.pack_start(self.scrollspace, False, False, 3)


    def on_add(self, arg1):
        print("Addwin opens...")
    



#        self.search.grid(column = 2, row = 2, sticky = W)

#        self.searchEntry = StringVar()
#        self.searchEntry = ttk.Entry(self.topwin, width = 30, textvariable=self.searchEntry)
#        self.searchEntry.grid(column = 1, row = 2, sticky = W)

#        ttk.Label(self.topwin, text = "File to analyse:").grid(column = 1, row = 1, sticky = W) 

#        self.add_task = Button(self.topwin, text="add", command = self.add_task_f, width=2, height=2)	
#        self.add_task.grid(column = 3, row = 3, sticky = W)

#        self.params = tktable.ArrayVar(self.topwin)
#        for y in range(6):
#            for x in range(6):
#                index = "%i,%i" % (y, x)
#                self.params[index] = index

#        self.table = tktable.Table(self.topwin,
#            rows = 6, cols = 6,
#            state = 'disabled',
#            width = 6, height = 6,
#            titlerows = 1, titlecols = 0,
#            roworigin = 0, colorigin = 0,
#            selectmode = 'browse', selecttype = 'row',
#            rowstretch = 'unset', colstrech = 'last',
#            flashmode = 'on',
#            variable = self.params)
#        self.table.pack(expand = 1, fill = 'both')
#        self.table.tag_configure('sel', background = 'yellow')
#        self.table.tag_configure('active', background = 'blue')
#        self.table.tag_configure('title', anchor = 'w', bg = 'red', relief = 'sunken')

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
        #self.out_queue.put(util.StatusMessage(content = "out OH MEIN GOTT WAS IST GESCHEHEN!?"))
        self.in_queue.put(util.StatusMessage(content = "in OH MEIN GOTT WAS IST GESCHEHEN!?"))
        self.in_queue.put(util.MESSAGE_EXIT)
        self.destroy()
        Gtk.main_quit()
        return True

