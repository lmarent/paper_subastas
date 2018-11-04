#auctioning_object.py

from enum import Enum 

class AuctioningObjectState(Enum):
    """
    States throughout which can pass the auctioning object.
    """
    NEW = 0
    VALID = 1
    SCHEDULED = 2
    ACTIVE = 3
    DONE = 4
    ERROR = 5

class AuctioningObject():
    """
    Defines common attributes and methods used for auctioning object. An auctioning object
    represents an abtract class of all objects  being exchanged in the auction.
    """

    def __init__(self, key, state=AuctioningObjectState.NEW):
        self.state = state
        self.key = key

    def set_state(self,state):
        """
        Change the object's state.
        """
        self.state = state
    
    def get_state(self):
        """
        Return object's state.
        """		
        return self.state

    def get_key(self):
        """
        Return object's key.
        """     
        return self.key
