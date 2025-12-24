

class BaseModule:
    def __init__(self):
        pass
    
    def get_info(self):
        return {"name": self.__class__.__name__, "module": self.__class__.__module__, "type": "base"}

    def initialize(self):
        raise NotImplementedError("Subclasses must implement initialize method")
    
    def deinitialize(self):
        raise NotImplementedError("Subclasses must implement deinitialize method")