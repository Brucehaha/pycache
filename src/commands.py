import time
import gevent
import threading 

from typing import TypedDict, Tuple

from src.cache import cache



def set_expire_command(key:int,ttl:int=30) -> str:
    """
    Set ttl for user id, when user id expired, then run delete function
    :param id: user id as the key of expiration
    :param ttl: expired time by second default: 30 seconds
    """

    def delete_when_expire(key):
        del cache.volatile_data[key]
        del cache.expiring[key]

    if key in cache.volatile_data:
        cache.expiring[key] = time.time() + int(ttl)
        # start a coroutine to delete expire key
        gevent.spawn_later(ttl, delete_when_expire, key)
        
        return 'ok'
    else:
        return f'no such key {key}'


def set_command(key:int, value:str):
    cache.volatile_data[key] = value
    cache.save_state()
    return 'ok'

def get_command(key: int) -> str:
    if value := cache.volatile_data.get(key, None):
        return True, value
    else:
        return False,'no such key {key}'










