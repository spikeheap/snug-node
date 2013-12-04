
class Sensor:
    """ An abstract sensor class. 
    
        All sensor classes should extend this base class.
        
        Author: Ryan Brooks 
    """
    
    def __init__(self, name, description, location):
        self.name = name
        self.description = description
        self.location = location