from enum import Enum, unique
import uuid

@unique
class MessageType(enum):
    none = 0
    text = 1
    command = 2

class _Message:
    type = none
    
class TextMessage(_Message):
    @unique
    class LogLevel(enum):
        error = 0
        warning = 1
        info = 2
        status = 3
        verbose = 4
        debug = 5
    def __init__(self, message, loglevel):
        self.message = message
        self.loglevel = loglevel
    message = ""
    loglevel = error
        
class CommandMessage(_Message):
    def __init__(self, command):
        self.command = command
        id = uuid.uuid1()
    command = ""
    id = 0
 
class CommandReturnMessage(_Message):
    def __init__(self, commandID, returnval):
        self.id = commandID
        self.val = returnval
    id = 0
    val = 0
