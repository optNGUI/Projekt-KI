### This script will take the parameter and call the core.
# Call this script with the correct arguments and the core will be 
# initialized.

#from  . import core.whatever
import importlib


def run(args):
    print(args)
    print("Exiting core...")



if __name__ == "__main__":
    print("Main entry point.")
    #print("run.py called with "+str(argv))
    
    # Evaluate command line arguments here and call main function.
    # arg0 = ....
    
    # _main(args)
    
    gui_name = "gui2"
    
    if True: # --gui flag
        test = importlib.import_module("."+gui_name+".test", package='opt_neuron')
        test.import_func()
