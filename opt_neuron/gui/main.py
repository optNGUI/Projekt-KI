# coding: utf8

import logging
from .. import util
from gi.repository import Gtk
from threading import Thread

logger = logging.getLogger(__name__)
__out_queue = None
__in_queue = None
__msg = None

__thread_intercom_q = None
__thread_intercom_msgid = []

def main(in_queue, out_queue):
    global __out_queue 
    global __in_queue 
    global __msg
    global __thread_intercom_q
    global __thread_intercom_msgid
    
    __out_queue = out_queue
    __in_queue = in_queue

    __thread_intercom_q = util.MessageQueue()

    main_window = engage_display()
    Gtk.main()
    
    receiver_t = Thread( target=receive )
    receiver_t.start()

def send_msg(*msg, thread_intercom_id = -1):
    if thread_intercom_id > -1:
        __thread_intercom_msgid.append(thread_intercom_id)
        print("setting " + str(thread_intercom_id))

    for i in msg:
        logger.debug("Sent message: {msg}".format(msg=str(msg)))
        __out_queue.put(i)
    
def __on_destroy():
    print("closing Gui!")
    __running = False
    #Thread( target=self.sendit, args=(util.MESSAGE_EXIT,) ).start()
    send_msg(util.MESSAGE_EXIT)
    Gtk.main_quit()

def receive():
    global __msg
    __msg_read = 0
    while not __msg_read:
        __msg = __in_queue.get()
        if __msg is not None:
            try:
                idx = __thread_intercom_msgid.index(__msg.cmd_id)
                __thread_intercom_q.put(__msg) # message is for thread things
            except:
                pass # nothing
            __msg_read = 1
    __msg_read = 0

# returns __msg, which is containing the msg after using receive()
def get_msg():
    global __msg
    receive()
    #print("__msg:")
    #print(__msg)
    #print("__msg.appendix:")
    #print(__msg.appendix)
    #print("__msg.content:")
    #print(__msg.content)
    #print("__msg.cmd_id:")
    #print(__msg.cmd_id)
    return __msg


def get_intercom_msg():
    lock = False
    receive()
    while not lock:
        i_msg = __thread_intercom_q.get()
        if i_msg is not None:
            lock = True

    print("MESSAGE: " + __msg.content)
    return i_msg

def flush_queues():
    while not __in_queue.empty():
        __in_queue.get()
    while not __thread_intercom_q.empty():
        __thread_intercom_q.get()

from . import addframe
from . import mainframe
from . import sshframe

def engage_display():
    mf = mainframe.MainFrame() #MainFrame(root)
    mf.connect("delete-event", Gtk.main_quit)
    mf.show_all()

    #af = addframe.AddFrame()
    #af.connect("delete-event", Gtk.main_quit)      Das zerstört nur die komplette GUI, wenn das x genutzt wird!
    #af.show_all()
    
    sf = sshframe.SshFrame(mf)
    sf.connect("delete-event", Gtk.main_quit)      #Das zerstört nur die komplette GUI, wenn das x genutzt wird!
    sf.show_all()

