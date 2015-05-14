### This script will take the parameter and initialize the core.


from .core import main as core_main
#import core.main
from . import __version__
import argparse, configparser, importlib, queue, logging, threading
import sys

def __outqueue_to_stdout(out_queue):
    def writer():
        while True:
            msg = out_queue.get()
            print(str(msg))
            out_queue.task_done()
    t = threading.Thread(target=writer)
    t.daemon = True
    t.start()



def run(*sysargs):
    print(sysargs)
    print('')
    # Step 1: Parse the arguments
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", help="Displays author and version info.",
                            action="store_true")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--gui", help="Loads a GUI.", const='gui', nargs='?')
    group.add_argument("--config", help="Loads a config file.")
    
    args = parser.parse_args(*sysargs)
    if args.version:
        print("Bachelor project: Optimizing biologically realistic neuron models")
        print("University of Luebeck, Germany")
        print("Supervisor: Christoph Metzner")
        print("Authors:")
        print("\tBereziak, Szymon")
        print("\tDannehl, Moritz")
        print("\tGirth, Chris")
        print("\tKalelioglu, Can")
        print("\tWolff, Julian")
        print("Version of installed opt_neuron package: {ver}\n".format(ver=__version__))
        return
    
    # Step 2: Load the config
    
    config = configparser.ConfigParser()
    tmp = config.read(args.config)
    if len(tmp) == 0:
        print("Config is empty!")
    del tmp
    
    
    
    logging_level = config.get('LOGGING', 'level', fallback='WARNING')
    logging_level = logging_level.upper()
    if logging_level not in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']:
        logging_level = logging.WARNING
    else:
        levels = {'CRITICAL' : logging.CRITICAL,
                    'ERROR' : logging.ERROR,
                    'WARNING' : logging.WARNING,
                    'INFO' : logging.INFO,
                    'DEBUG' : logging.DEBUG
                }
        logging_level = levels[logging_level]
        del levels
    logfilename = config.get('LOGGING', 'logfile', fallback='logfile.txt')
    
    
    
    # Initialize logging
    logging.basicConfig(filename=logfilename, level=logging_level, filemode='w')
    logging.debug("First test")
    
    # Initialize queues
    in_queue = queue.Queue()
    out_queue = queue.Queue()
    
    # Initialize Core, now waiting for commands
    core_thread = core_main.init(in_queue, out_queue)
    

    
    # Step 3: Depending on args/config do one of the following:
        # a. Load the GUI/CLI and wait for input
        
    if args.gui:
        gui = importlib.import_module('opt_neuron.'+args.gui, package='opt_neuron')
        guimain = importlib.import_module('opt_neuron.'+args.gui+'.main', package='opt_neuron')
        guimain.main()
        
        
        # b. No GUI/CLI: Execute the commands in the config and set output to stdout
    else:
        #__outqueue_to_stdout(out_queue)
        pass
    
    print("This is an echo input. If you wish to exit, type 'exit'")
    
    break_ = False
    for line in sys.stdin:
        in_queue.put(line)
        while True:
            try:
                msg = out_queue.get_nowait()
            except queue.Empty:
                break
            if msg.startswith('TERMINATE'):
                break_=True
            print(msg)
        if break_:
            break
    
    # Step 4: Wait for the core main loop to join
    core_thread.join()
    
