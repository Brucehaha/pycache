import os
import pickle

from src.settings import DB_PATH

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
        pickle.dump({"volatile_data": self.volatile_data}, open(DB_PATH, 'wb'))
    
    def load_state(self):
        if os.path.exists(DB_PATH):
            state = pickle.load(open(DB_PATH, 'rb'))
            self.volatile_data = state['volatile_data']


         


cache = Cache()