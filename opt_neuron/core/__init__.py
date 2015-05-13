__all__ = []
__out_queue = None
__terminate = False
### Init for core.
import logging
from threading import Thread
from . import *
logger = logging.getLogger('core')


# List here every submodule which should be imported via 'from core import *' statement.

def main_loop(in_queue):
    logger.debug('in_queue listener started')
    while not __terminate:
        msg = in_queue.get()
        logger.debug("Received message: {msg}".format(msg=str(msg)))
        # Do something (parse the message)..
        parse_msg(msg)
        
        # Finally, the task is done
        in_queue.task_done()
    logger.info("Core exited")
    
def send_msg(msg):
    __out_queue.put(msg)
        
def parse_msg(msg):
    global __terminate
    if msg.startswith('exit'):
        logger.info("Terminating Core...")
        __terminate = True
        send_msg('TERMINATE')
        
    # First a simple echo
    send_msg(msg)
    
    
__runOnce=False

def init(in_queue, out_queue):
    global __runOnce
    global __out_queue
    if __runOnce:
        logger.warning('Core init after already initialized')
        return
    logger.debug("CORE INIT")
    
    # Start queue listener
    __out_queue = out_queue
    mainloop = Thread(target=main_loop, args=(in_queue,))
    mainloop.start()
    __runOnce=True
    return mainloop
