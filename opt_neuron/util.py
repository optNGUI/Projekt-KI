"""
Contains utility.
"""
from abc import ABCMeta
from abc import abstractmethod
from enum import Enum
from queue import PriorityQueue
from sys import platform as _platform

import logging
logger = logging.getLogger(__name__)



class MessageType(Enum):
    STATUS = 1,
    COMMAND = 2,
    RETVAL = 3,


class Message(metaclass=ABCMeta):
    """
    Message encapsulates a message.
    A message has got a type (subclassed), an id, a priority and \
    content, of course.
    """
    _id_  = 0
    
    def __init__(self, content, priority=0):
        self.__content = content
        self.__priority = priority
        self.__id = Message._id_
        Message._id_ += 1
    
    @property
    @abstractmethod
    def type(self):
        """
        To be overwritten in subclasses. Should return a MessageType object.
        """
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
        if cmd_msg is not None:
            self.__cmd_id = cmd_msg.id
        else:
            self.__cmd_id = -1
        self.__appendix = appendix
        if content is None:
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
    """
    Returns a message which indicates that the previous command failed.
    Fancy output by Julian.
    """
    if status:
        if _platform == "linux" or _platform == "linux2":
            return RetValMessage(msg, appendix = False, content="\x1b[1;31m"+status+"\x1b[39;49m")
        else:
            return RetValMessage(msg, appendix = False, content="ERROR: "+status)
    else:
        if _platform == "linux" or _platform == "linux2":
            return RetValMessage(msg, appendix = False, content="\x1b[1;31mERROR\x1b[39;49m")
        else:
            return RetValMessage(msg, appendix = False, content="ERROR")
            

def MESSAGE_SUCCESS(msg, status=None):
    """
    Returns a message which indicates that the previous command succeded.
    Fancy output by Julian.
    """
    if status:
        if _platform == "linux" or _platform == "linux2":
            return RetValMessage(msg, appendix = True, content="\x1b[1;32m"+status+"\x1b[39;49m")
        else:
            return RetValMessage(msg, appendix = True, content="SUCCESS: "+status)
    else:
        return RetValMessage(msg, appendix = True, content="")


class MessageQueue(PriorityQueue):
    """
    Adaption of the PriorityQueue class.
    Only objects of type Message can be put in this queue as the name already suggests.
    Every sent message will be logged (Level: DEBUG)
    """
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
        
