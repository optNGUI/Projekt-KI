### This script will take the parameter and call the core.
# Call this script with the correct arguments and the core will be 
# initialized.



def run(*args):
    print("run.run called with "+str(args))
        
    # Evaluate arguments and initialize the IO streams and the core
    # TODO what arguments?
    
    if args[0] == "Von der GUI":
        print("Call kam von GUI zurück")
    if args[0] == "call gui":
        import opt_neuron.gui.test as test
        print("Calling GUI...")
        test.start_calc()   
