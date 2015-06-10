from .. import util
import subprocess
import logging, uuid, time, sys
from io import StringIO
from contextlib import redirect_stdout

logger = logging.getLogger(__name__)

password = ''


def call(host, passwd, command):
    try:
        ssh = subprocess.check_output(['sshpass','-p', passwd, 'ssh', '-o', '''PubkeyAuthentication=no''', host,
                                command],
            shell=False,
            universal_newlines= True)
        return ssh
    except subprocess.CalledProcessError:
        pass
    
    
# TODO: Annotation: Cache similar calls
def start_net(host,net,analysis,*args):
    """Starts the net with the given parameters and
    returns the fitness value calculated by the
    analysis script.
    """
    
    fnum = str(uuid.uuid4())
    
    
    # run net and wait for the process to terminate
    commandlist = [net,]
    if args:
        for arg in args: 
            commandlist.extend(arg)
    command = " ".join(commandlist)
    
    logger.warning("executing "+command)
    call(host,password,command)

    command = analysis
    val = call(host,password,command)
    print (val)
        
    return 0
