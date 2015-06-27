# coding: utf8

import logging
from .. import util
from gi.repository import Gtk
from threading import Thread

logger = logging.getLogger(__name__)
__out_queue = None
__in_queue = None
__msg = None
__running = 1

def main(in_queue, out_queue):
    global __out_queue 
    global __in_queue 
    global __msg
    global __running
    __out_queue = out_queue
    __in_queue = in_queue

    testWin = test(__in_queue, __out_queue)
    Gtk.main()
    
    self.receiver_t = Thread( target=self.receive )
    self.receiver_t.start()

def send_msg(*msg):
    for i in msg:
        logger.debug("Sent message: {msg}".format(msg=str(msg)))
        __out_queue.put(i)    
    
def __on_destroy():
    print("closing Gui!")
    __running = False
    Thread( target=self.sendit, args=(util.MESSAGE_EXIT,) ).start()
    Gtk.main_quit()
    print("asd")

def receive():
    print("thread started")
    while __running:
        print("waiting...")
        __msg = __in_queue.get()
        print("message received!")
        print(msg)

        alert = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, msg)
        alert.connect("delete-event", alert.destroy)
        alert.run()
        print("msg box closed")
        alert.destroy()

# returns __msg, which is containing the msg after using receive()     
def get_msg():
    while __msg is None:
        receive()
    return __msg
    
# sets _msg to 'None', use after 'get_msg', to secure that get_msg is working correctly!!
def clear_msg():
    __msg = None
    
from . import addframe
from . import mainframe
from . import sshframe


def test(in_queue, out_queue):   
    mf = mainframe.MainFrame(in_queue, out_queue) #MainFrame(root)
    mf.connect("delete-event", Gtk.main_quit)
    mf.show_all()

    af = addframe.AddFrame()
    #af.connect("delete-event", Gtk.main_quit)      Das zerstört nur die komplette GUI, wenn das x genutzt wird!
    af.show_all()
    
    sf = sshframe.SshFrame()
    #sf.connect("delete-event", Gtk.main_quit)      Das zerstört nur die komplette GUI, wenn das x genutzt wird!
    sf.show_all()

