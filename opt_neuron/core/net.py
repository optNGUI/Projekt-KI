"""

"""

from .. import util
import subprocess
import logging, uuid, time, sys, os
from io import StringIO
from contextlib import redirect_stdout
from functools import lru_cache

logger = logging.getLogger(__name__)

password = ''


def call(host, passwd, command):
    try:
        FNULL = open(os.devnull, 'w')
        ssh = subprocess.check_output(['sshpass','-p', passwd, 'ssh', '-o', '''PubkeyAuthentication=no''', host,
                                command],
            shell=False,
            universal_newlines= True)
        return ssh
    except subprocess.CalledProcessError as e:
        logger.error(str(e))
        return e
    
    
# TODO: Annotation: Cache similar calls
@lru_cache(maxsize=10000)
def start_net(host,net,analysis,*args):
    """Starts the net with the given parameters and
    returns the fitness value calculated by the
    analysis script.
    """
    
    fnum = str(uuid.uuid4())
    
    logger.info("starting net "+fnum)
    
    logger.debug(str(args))
    
    # run net and wait for the process to terminate
    commandlist = [net,]
    if args:
        for arg in args: 
            commandlist.append(str(arg))
             
    command = " ".join(commandlist)+" "+fnum
    
    val = call(host,password,command)
    
    if isinstance(val,subprocess.CalledProcessError):
        start_net.cache_clear()
        return val
    
    command = analysis+" "+fnum
    
    val = call(host,password,command)

    if isinstance(val,subprocess.CalledProcessError):
        start_net.cache_clear()
        return val
        
    val = val[:val.rfind('\n')]
    val = val[val.rfind('\n'):]

    return float(val)
