#!/usr/bin/env/

### Calls the opt_neuron package. ###

# Needing an argparser

import opt_neuron
from opt_neuron import __version__
import opt_neuron.run
import argparse, configparser, importlib, sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", help="Displays author and version info.",
                            action="store_true")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--gui", help="Loads a GUI.", const='gui', nargs='?')
    group.add_argument("--config", help="Loads a config file.")
    
    args = parser.parse_args()
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
    #print(args)
    if args.config:
        config = configparser.ConfigParser()
        config.read(args.config)
        #print(config.sections())
        general = config['GENERAL']
        input_method = general.get('input', "stdin")
        run_args = config['RUN']['command line']
        if input_method == 'stdin':
            input_method = sys.stdin
        else:
            input_method = open(input_method, mode='r', buffering=1, newline=None)
        for line in input_method:
            print(line.rstrip("\r\n")+'X')
        
        opt_neuron.run.run(run_args)
    
    if args.gui:
        gui = importlib.import_module('opt_neuron.'+args.gui, package='opt_neuron')
        test = importlib.import_module('opt_neuron.'+args.gui+'.test', package='opt_neuron')
        test.start_calc()
