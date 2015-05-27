# coding: utf8

### This file contains the main entry point for the core ###

import logging, configparser
from threading import Thread
from .. import util
import shlex
from . import net

logger = logging.getLogger(__name__)
config = None
__algorithm_names = None
__algorithm_funcs = None
__algorithm_argspec = None



__out_queue = None
__terminate = False # Indicates whether the core shall exit

def send_msg(*msg):
    for i in msg:
        logger.debug("Sent message: {msg}".format(msg=str(msg)))
        __out_queue.put(i)
    

from . import algorithms


def main_loop(in_queue):
    global __algorithm_argspec
    global __algorithm_funcs
    global __algorithm_names
    logger.debug('in_queue listener started')
    tmp = algorithms.list_of_algorithms()
    __algorithm_names = [i[0] for i in tmp]
    __algorithm_funcs = [i[1] for i in tmp]
    __algorithm_argspec = [i[2] for i in tmp]
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
    
    if msg == util.MESSAGE_EXIT:
        logger.info("Terminating Core...")
        __terminate = True
        send_msg(util.MESSAGE_EXIT)
    
    elif isinstance(msg, util.CommandMessage):
        
        content = shlex.split(msg.content)
        
        if content[0] == 'ssh':
            host = config.get("SSH", "host")
            command = config.get("SSH", "net")+''.join([str(i)+" " for i in content[1:]])+"&& "+config.get("SSH", "analysis")
            net.call(host,command)
    
        if content[0] == 'get':
            if content[1] == 'hello_world':
                send_msg(util.StatusMessage(content = 'Hello World'))
            elif content[1] == 'algorithms':
                send_msg(util.RetValMessage(msg, appendix=algorithms.list_of_algorithms()))
            elif content[1] == 'config':
                if len(content) < 3:
                    send_msg(util.RetValMessage(msg, appendix = config))
                elif len(content) < 4:
                    try:
                        send_msg(util.RetValMessage(msg, appendix = config.options(content[2])))
                    except configparser.NoSectionError:
                        send_msg(util.RetValMessage(msg, appendix = []))
                else:
                    try:
                        send_msg(util.RetValMessage(msg, appendix = config.get(content[2],content[3])))
                    except (configparser.NoSectionError, configparser.NoOptionError):
                        send_msg(util.RetValMessage(msg, appendix = []))
                
        elif content[0] == 'set':
            if content[1] == 'config':
                if len(content) < 5:
                    send_msg(util.MESSAGE_FAILURE(msg))
                else:
                    try: 
                        config.add_section(content[2])
                    except configparser.DuplicateSectionError:
                        pass
                    config.set(content[2],content[3],content[4])
                    send_msg(util.RetValMessage(msg, appendix = True))
                    
                    
             #HierKannManWasErgänzen. Ui....Tolles Ding...
             
        elif content[0] == 'save':
            if content[1] == 'config':
                config.write(open(config.get('INTERNAL','configPath'),'w'))
         
        elif content[0] == 'start':
            if content[1] in __algorithm_names:
                    func = algorithms.ThreadedAlgorithm(__algorithm_funcs[__algorithm_names.index(content[1])])
                    func(*content[2:])
            else:
                send_msg(*util.MESSAGE_FAILURE(msg, 'could not identify algorithm '+content[1]))
                
        elif content[0] == 'echo':
            send_msg(util.RetValMessage(msg, appendix = content[1]))
        
        else:
            send_msg(util.MESSAGE_FAILURE(msg))
        
__runOnce=False

def init(in_queue, out_queue, config_):
    global __runOnce
    global __out_queue
    global config
    if __runOnce:
        logger.warning('Core init after already initialized')
        return
    logger.debug("CORE INIT")
    config = config_
    # Start queue listener
    __out_queue = out_queue
    mainloop = Thread(target=main_loop, args=(in_queue,))
    mainloop.start()
    __runOnce=True
    return mainloop
