from .. import util
import subprocess, sys, threading, time

def call(host,command):
    out = open('/home/dannehl/out.txt', 'w')
    ssh = subprocess.Popen(['ssh', '617529@ssh-gate.informatik.uni-luebeck.de', '-i', '/home/dannehl/.ssh/id_rsa'],
        stdin=subprocess.PIPE, 
        stdout=out, 
        stderr=out, 
        shell=False,
        universal_newlines= True)
    ssh.stdin.write('ls -la\n')
    time.sleep(1)
    ssh.stdin.write('ls\n')
    #tmp = ssh.communicate('ls -la')
    #tmp = ssh.communicate('ls -la')
    #ssh.communicate(bytes('exit', 'utf-8'))
    #print(str(tmp))

# TODO: Annotation: Cache similar calls
def start_net(arg0, arg1, arg2, arg3):
    """Starts the net with the four parameters and
    returns the fitness value calculated by the
    analysis script.
    """
    return 0