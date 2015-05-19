### This file contains the main entry point for the core ###

import logging
from threading import Thread
from .. import util

logger = logging.getLogger(__name__)


__out_queue = None
__terminate = False # Indicates whether the core shall exit

def send_msg(msg):
    logger.debug("Sent message: {msg}".format(msg=str(msg)))
    __out_queue.put(msg)
    

from . import algorithms


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
    

        
def parse_msg(msg):
    global __terminate
    content = msg.content.split(' ', 1)
    
    if msg == util.EXIT_MESSAGE:
        logger.info("Terminating Core...")
        __terminate = True
        send_msg(util.EXIT_MESSAGE)
    
    elif content[0] == 'get':
        if content[1] == 'hello_world':
            send_msg(util.StatusMessage(content = 'Hello World'))
         #...
    
    elif content[0] == 'start':
        if content[1] == 'dummy':
            dummy = algorithms.ThreadedAlgorithm(algorithms.dummy_algorithm)
            dummy('TEST')
            
    elif content[0] == 'echo':
        send_msg(util.CommandMessage(content = ('ECHO: '+content[1])))
    
    
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
