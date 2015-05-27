from .. import util
import subprocess, sys, threading

def call(host,command):
    terminate = False
    def writer():
        #while not terminate:
            sys.stdin.write(input('>>>>>'))
    t = threading.Thread(target=writer)
    t.daemon = True
    t.start()
    ssh = subprocess.Popen(["ssh", host, command],
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        shell=True, 
        universal_newlines=True)
    result = ssh.stdout.readlines()
    if result == []:
        error = ssh.stderr.readlines()
        main.send_msg(util.StatusMessage('SSH Error:\n'+error))
    return result