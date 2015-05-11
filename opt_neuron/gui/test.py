###  This file is used by the core dev team for testing purposes. ###

import subprocess

def command_line():
    # Call by command line
    try:
        subprocess.call(["../run.py", "argument0"], shell=False)
    except PermissionError:
        print("PermissionError: Permission denied")
        print("Maybe executable flag is not set?")
    
    
    
def import_func():
    # Call by import and directly call the function
    from .. import run
    run.run("1234")

if __name__ == "__main__":
    print("Called gui.test")
    import_func()
