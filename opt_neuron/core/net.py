from .. import util
import subprocess, sys, threading, time

def call(host,command):
    out = open('out.txt', 'w')
    ssh = subprocess.Popen(['sshpass','-p', 'rdx556', 'ssh', '-o', '''PubkeyAuthentication=no''', 'bachelor1@localhost',
                            'cd ~/acnet2 && genesis acnet2.g 4 5 6 7 blubdidub'],
        stdin=subprocess.PIPE, 
        stdout=out, 
        stderr=out, 
        shell=False,
        universal_newlines= True)