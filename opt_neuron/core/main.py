# coding: utf8

### This file contains the main entry point for the core ###

import logging, configparser, getpass, sys, subprocess
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

def send_msg(msg):
    try:
        for i in msg:
            logger.debug("Sent message: {msg}".format(msg=str(i)))
            __out_queue.put(i)
    except TypeError:
        logger.debug("Sent message: {msg}".format(msg=str(msg)))
        __out_queue.put(msg)
    

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
    global __algorithm_names
    global __algorithm_funcs
    global __algorithm_argspec
    
    if msg == util.MESSAGE_EXIT:
        logger.info("Terminating Core...")
        __terminate = True
        send_msg(util.MESSAGE_EXIT)
    
    elif isinstance(msg, util.CommandMessage):
        
        #default return message is true meaning "yep, I handled that message."
        retval = util.MESSAGE_SUCCESS(msg)
        
        content = shlex.split(msg.content)
        
        if len(content) > 0:
        
            if content[0] == 'help':
                if(len(content)<2):
                    retval = util.RetValMessage(msg,
                        '\n\nget algorithms \t\t\t\t- returns a list of implemented optimizing algorithms\n\n'+\
                        'get algorithms <name> \t\t\t- returns a list of possible arguments for the algorithm with the given name\n\n'+\
                        'get config \t\t\t\t- returns a list of existing sections in the loaded config file\n\n'+\
                        'get config <section> \t\t\t- returns a list of available options in the given section\n\n'+\
                        'get config <section> <option> \t\t- returns the value of the given option\n\n'+\
                        'set config <section> <option> <value> \t- sets the given option in the given section to the given value\n\n'+\
                        'set password \t\t\t\t- opens a password prompt (for setting the SSH password to the server running the neural net)\n\n'+\
                        'save config \t\t\t\t- saves the config\n\n'+\
                        'start <algorithm> <params...> \t\t- starts a net optimization using the algorithm with the given name and the given params\n\n'
                    )
            
            elif content[0] == 'get' and len(content) > 1:
                if content[1] == 'algorithms':
                    tmp = algorithms.list_of_algorithms()
                    __algorithm_names = [i[0] for i in tmp]
                    __algorithm_funcs = [i[1] for i in tmp]
                    __algorithm_argspec = [i[2] for i in tmp]
                    retval = util.RetValMessage(msg, appendix=[__algorithm_names,__algorithm_funcs,__algorithm_argspec], content=str(__algorithm_names))
                    if(len(content) > 2 and (content[2] in __algorithm_names)):
                        for i in range(len(__algorithm_names)):
                            if(content[2] == __algorithm_names[i]):
                                line = content[2]+" "
                                if(__algorithm_argspec[i].defaults is not None):
                                    indoffset = len(__algorithm_argspec[i].args[1:])-len(__algorithm_argspec[i].defaults);
                                else:
                                    indoffset = len(__algorithm_argspec[i].args[1:])
                                for ind,arg in enumerate(__algorithm_argspec[i].args[1:]):
                                    line += arg
                                    if indoffset <= ind:
                                        line += "="+str(__algorithm_argspec[i].defaults[ind-indoffset])
                                    line += " "
                                retval = util.RetValMessage(msg, appendix=[__algorithm_names[i],__algorithm_funcs[i],__algorithm_argspec[i]], content=line)
                elif content[1] == 'config':
                    if len(content) < 3:
                        retval = util.RetValMessage(msg, appendix = config, content = str(config.sections()))
                    elif len(content) < 4:
                        try:
                            retval = util.RetValMessage(msg, appendix = config.options(content[2]))
                        except configparser.NoSectionError:
                            retval = util.RetValMessage(msg, appendix = [], content = "no options here...")
                    else:
                        try:
                            retval = util.RetValMessage(msg, appendix = config.get(content[2],content[3]))
                        except (configparser.NoSectionError, configparser.NoOptionError):
                            retval = util.RetValMessage(msg, appendix = [], content = "no value here...")
                else:
                    retval = util.MESSAGE_FAILURE(msg,"cannot get "+content[1])
                    
            elif content[0] == 'set' and len(content) > 1:
                if content[1] == 'config':
                    if len(content) < 5:
                        retval = util.MESSAGE_FAILURE(msg,"not enough arguments")
                    else:
                        try: 
                            config.add_section(content[2])
                        except configparser.DuplicateSectionError:
                            pass
                        config.set(content[2],content[3],content[4])
                        retval = util.MESSAGE_SUCCESS(msg,"new value: "+content[4])
                elif content[1] == 'password':
                    if len(content) < 3:
                        net.password = getpass.getpass("password: ")
                    else:
                        net.password = content[2]
                    retval = util.MESSAGE_SUCCESS(msg,"password set")
                else:
                    retval = util.MESSAGE_FAILURE(msg,"cannot set "+content[1])

                
            elif content[0] == 'save' and len(content) > 1:
                if content[1] == 'config':
                    config.write(open(config.get('INTERNAL','configPath'),'w'))
            
            elif content[0] == 'start' and len(content) > 1:
                if content[1] in __algorithm_names:
                    func = algorithms.ThreadedAlgorithm(
                        msg,
                        config.get("SSH","host"),
                        config.get("SSH","net"),
                        config.get("SSH","analysis"),
                        __algorithm_funcs[__algorithm_names.index(content[1])])
                    if len(content) > 2:
                        retval = util.RetValMessage(msg, appendix = func(*content[2:]), content="optimization started in new thread...\ncall 'stop "+str(msg.id)+"' to terminate the computation.")
                    else:
                        retval = util.MESSAGE_FAILURE(msg, "not enough arguments. call 'get algorithms "+content[1]+"' for further information.")
                else:
                    retval = util.MESSAGE_FAILURE(msg, 'could not identify algorithm '+content[1])
                    
            elif content[0] == 'echo':
                retval = util.RetValMessage(msg, appendix = content[1])
            
            elif content[0] == 'stop' and len(content) > 1:
                try:
                    if algorithms.kill(int(content[1])):
                        retval = util.MESSAGE_SUCCESS(msg,"optimization "+str(content[1])+" is going to terminate...")
                    else:
                        retval = util.MESSAGE_SUCCESS(msg,"optimization "+str(content[1])+" already terminated...")
                except KeyError:
                    retval = util.MESSAGE_FAILURE(msg,"optimization "+str(content[1])+" has not been started yet")
                
            else:
                retval = util.MESSAGE_FAILURE(msg,"unknown command "+content[0]+" for this number of arguments")
            
        #send return message
        send_msg(retval)
            
        
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
