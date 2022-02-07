import os
import time
import pickle
import gevent
from src.settings import DB_PATH


class Cache:
    """
    Simple Cache System l
    oad_state from binay file and 
    Save_state is to save valatile data from memory to file
    """
    volatile_data = {}
    expiring = {}

    def __init__(self):
        self.load_state() # load cache from file
        self.clean_expire()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.save_state() # save to file

    def save_state(self):
        pickle.dump({"volatile_data": self.volatile_data}, open(DB_PATH, 'wb'))
    
    def load_state(self):
        if os.path.exists(DB_PATH):
            state = pickle.load(open(DB_PATH, 'rb'))
            self.volatile_data = state['volatile_data']

    def clean_expire(self):
        """
        clear expired item from self.expiring and self.volatile_data
        set expiration for non expired item 
        """
        expired = set()
        now = time.time()
        for id, ttl in self.expiring.items():
            if ttl <= now: # expired
                expired.add(id)
                if id in self.volatile_data:
                    del self.volatile_data[id]
            else: # not expired yet
                def delete_when_expire(e, cache_obj):
                    del cache_obj.volatile_data[e]
                    del cache_obj.expiring[e]
                expired_in = ttl - time.time()
                print('expire in %s' % expired_in)
                gevent.spawn_later(expired_in, delete_when_expire, id, self)
        for exp in expired:
            del self.expiring[exp]
                    
cache = Cache()