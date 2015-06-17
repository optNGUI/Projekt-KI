# coding: utf8

import logging
from .. import util
from gi.repository import Gtk

logger = logging.getLogger(__name__)
__out_queue = None

def main(out_queue, in_queue):
    global __out_queue
    __out_queue = out_queue
    testWin = test(in_queue, out_queue)
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

    af = addframe.AddFrame(in_queue,out_queue)
    af.connect("delete-event", Gtk.main_quit)
    af.show_all()
    
    sf = sshframe.SshFrame(in_queue,out_queue)
    sf.connect("delete-event", Gtk.main_quit)
    sf.show_all()

if __name__ == "__main__":
    test = main(out_queue,in_queue)

