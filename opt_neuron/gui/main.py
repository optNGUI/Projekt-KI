# coding: utf8

import logging
from .. import util
from gi.repository import Gtk

logger = logging.getLogger(__name__)
__out_queue = None
__in_queue = None

def main(in_queue, out_queue):
    global __out_queue 
    global __in_queue 
    __out_queue = out_queue
    __in_queue = in_queue

    testWin = test(__in_queue, __out_queue)
    Gtk.main()
    
def send_msg(*msg):
    for i in msg:
        logger.debug("Sent message: {msg}".format(msg=str(msg)))
        __out_queue.put(i)
        
from . import addframe
from . import mainframe
from . import sshframe


def test(in_queue, out_queue):   
    mf = mainframe.MainFrame(in_queue, out_queue) #MainFrame(root)
    mf.connect("delete-event", Gtk.main_quit)
    mf.show_all()

    af = addframe.AddFrame(in_queue)
    af.connect("delete-event", Gtk.main_quit)
    af.show_all()
    
    sf = sshframe.SshFrame(in_queue)
    sf.connect("delete-event", Gtk.main_quit)
    sf.show_all()
