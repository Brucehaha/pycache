import pickle
import os.path


class Cache:
    """
    Simpale Cache System l
    oad_state from binay file and 
    Save_state is to save valatile data from memory to file
    """
    volatile_data = {}

    def __init__(self):
        self.load_state() # load cache from file
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.save_state() # save to file

    def save_sate(self):
        pass
    
    def load_state(self):
        pass 


cache = Cache()