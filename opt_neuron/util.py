from abc import ABCMeta
from abc import abstractmethod
from enum import Enum
from queue import PriorityQueue

import logging
logger = logging.getLogger(__name__)



class MessageType(Enum):
    STATUS = 1,
    COMMAND = 2,
    RETVAL = 3,


class Message(metaclass=ABCMeta):
    _id_  = 0
    
    def __init__(self, content, priority=0):
        self.__content = content
        self.__priority = priority
        self.__id = Message._id_
        Message._id_ += 1
    
    @property
    @abstractmethod
    def type(self):
        return self.__type
        
    @property
    def id(self):
        return self.__id
    
    
    @property
    def priority(self):
        return self.__priority
        
    @property
    def content(self):
        return self.__content
    
    def __repr__(self):
        return type(self).__name__ + \
                '(content=' + repr(self.content) + \
                ', priority=' + str(self.priority) + ')'
    
    def __eq__(self, other):
        return self.content == other.content and \
                self.priority == other.priority and \
                self.type == other.type
    
    def __lt__(self, other): # Just for the PriorityQueue
        return True


class CommandMessage(Message):
    def __init__(self, content, priority=0):
        if type(content) is not str:
            logger.warning('Ey du Vollhorst')
            raise TypeError("Expected string, but got " + \
                    str(type(content)))
        super(CommandMessage, self).__init__(content=content, priority=priority)
    
    
    def type(self):
        return MessageType.COMMAND

class StatusMessage(Message):
    def type(self):
        return MessageType.STATUS


class RetValMessage(Message):
    def __init__(self, cmd_msg, appendix=None, content=None, priority=0):
        self.__cmd_id = cmd_msg.id
        self.__appendix = appendix
        if content==None:
            content = str(appendix)
        super(RetValMessage, self).__init__(content=content, priority=priority)
        
    @property
    def appendix(self):
        return self.__appendix
    
    
    @property
    def cmd_id(self):
        return self.__cmd_id
    
    def type(self):
        return MessageType.RETVAL

MESSAGE_EXIT = CommandMessage('CORE-EXIT', priority=-9001)

def MESSAGE_FAILURE(msg, status=None):
    if status:
        statusmsg = StatusMessage("FAILURE: "+status)
        return (RetValMessage(msg, appendix = False),statusmsg)
    else:
        return RetValMessage(msg, appendix = False)


class MessageQueue(PriorityQueue):
    def put(self, item, block=True, timeout=None):
        if not isinstance(item, Message) :
            logger.warning(str(type(item)))
            logger.warning('Ey du Vollhorst!')
            raise TypeError("Expected Message, but got "
                    + str(type(item)))
        patricia = (item.priority, item)
        logger.debug("MessageQueue: Sending tuple: " + str(patricia))
        super(MessageQueue, self).put(patricia, block=block, timeout=timeout)
        
    def get(self, block=True, timeout=None):
        return (super(MessageQueue, self).get(block=block, timeout=timeout))[1]
        
