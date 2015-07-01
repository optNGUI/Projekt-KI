### This script will take the parameter and initialize the core.


from .core import main as core_main
#import core.main
from . import __version__
from . import util
import argparse, configparser, importlib, logging, threading, queue, traceback
import sys, getpass

shell = None


def run(*sysargs):
    # Step 1: Parse the arguments
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", help="Displays author and version info.",
                            action="store_true")
    parser.add_argument("--gui", help="Loads a GUI.", const='gui', nargs='?')
    parser.add_argument("--config", help="Loads a config file.")
    
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
    
    if args.config is None:
        args.config = 'conf.ini'
    tmp = config.read(args.config)
    if len(tmp) == 0:
        print("Config is empty!")
    del tmp
    
    try: 
        config.add_section('INTERNAL')
    except configparser.DuplicateSectionError:
        pass
    config.set('INTERNAL','configPath',args.config)
   
    logging_level = config.get('LOGGING', 'level', fallback='WARNING')
    logging_level = logging_level.upper()
    if logging_level not in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']:
        logging_level = logging.DEBUG
    else:
        levels = {'CRITICAL' : logging.CRITICAL,
                    'ERROR' : logging.ERROR,
                    'WARNING' : logging.WARNING,
                    'INFO' : logging.INFO,
                    'DEBUG' : logging.DEBUG
                }
        logging_level = levels[logging_level]
        del levels
    logfilename = config.get('LOGGING', 'logfile', fallback='logfile.log')
    # Load initial commands
    commands = config.get('RUN', 'command line', fallback='echo Hello World')
    commands = commands.split(',')
    commands = [command.lstrip(' ').rstrip(' ') for command in commands]
    
    
    # Initialize logging
    logging.basicConfig(filename=logfilename, level=logging_level, filemode='w')
    logging.debug("First test")
    logger = logging.getLogger(__name__)
    
    # Initialize queues
    in_queue = util.MessageQueue()
    out_queue = util.MessageQueue()
    
    # Initialize Core, now waiting for commands
    core_thread = core_main.init(in_queue, out_queue, config)
    

    
    # Step 3: Depending on args/config do one of the following:
        # a. Load the GUI/CLI and wait for input
        
    if args.gui:
        #gui = importlib.import_module('opt_neuron.'+args.gui, package='opt_neuron')
        #guimain = importlib.import_module('opt_neuron.'+args.gui+'.main', package='opt_neuron')
        #guimain.main()
        try:
            from .gui import main as gui_main
            threading.Thread(target=gui_main.main, args=(out_queue, in_queue,)).start()
            
            #gui_main.main(out_queue, in_queue)
        except Exception as e:
            print("###\n!!! GUI failed !!!" )
            traceback.print_exc()
            print('\n')
        
        
        # b. No GUI/CLI: Execute the commands in the config and set output to stdout
    else:
        #__outqueue_to_stdout(out_queue)
#        pass
        
       # Start simple listener
        def listener():
            t = None
            while True:
                msg = out_queue.get()
                if isinstance(msg,util.RetValMessage):
                    print('\nreturn: '+msg.content+'\n>', end="")
                    if(t is None or not t.is_alive()):
                        t = threading.Thread(target = shell.cmdloop)#wait for new command after a return message was received
                        t.daemon = True
                        t.start()
                else:
                    print('\n'+msg.content+'\n>', end="")
                out_queue.task_done()
        t = threading.Thread(target=listener)
        t.daemon = True # This listener won't block the whole process
        t.start()
        import cmd

        print("Executing commands from config...")
        for command in commands:
            in_queue.put(util.CommandMessage(content=command))
    
    
        class SimpleShell(cmd.Cmd):
            intro = ''
            prompt = '>'
            
            def default(self, arg):
                in_queue.put(util.CommandMessage(content=arg))
            
            def do_exit(self, line):
                in_queue.put(util.MESSAGE_EXIT)
                return True
        
            def do_EOF(self, line):
                in_queue.put(util.MESSAGE_EXIT)
        
            def postcmd(self, stop, line):
                return True
    
        shell = SimpleShell()
        print('\nWelcome to the default Command Line Interface. '+ \
            'You may enter a command now, e.g. "echo MESSAGE"\n' +\
            'To exit the program, type "exit" or hit Ctrl-D\n')
        shell.cmdloop()
    
    
    
    
    #for line in sys.stdin:
        #if line.rstrip('\r\n') == 'exit':
            #in_queue.put(util.EXIT_MESSAGE)
            #break
        #else:
            #msg = util.CommandMessage(content = line.rstrip('\r\n'))
            #in_queue.put(msg)
        #sys.stdout
    #else: # In case the for-loop was terminated using EOL character (Ctrl-D)
        #in_queue.put(util.EXIT_MESSAGE)
    
    
    # Step 4: Wait for the core main loop to join (should not take too long)
    core_thread.join()
    
