import os
import time
import gevent

from src.cache import cache
from src.commands import set_expire_command, set_command, get_command


def test_save_and_load_state_succeed(tmp_path):
    """
    Given set key value into cache
    When save state
    Then data will saved to right file position and can bed loaded out sucessfully
    """
    cache.volatile_data['test'] = 9999999
    cache.save_state()
    assert os.path.exists(tmp_path)
    del cache.volatile_data['test']
    cache.load_state()
    assert isinstance(cache.volatile_data['test'], int)
    assert cache.volatile_data['test'] == 9999999


def test_cache_expired_and_removed_succeed(tmp_path):
    """
    Given when store data in to cache with exipred time in 1 second
    When clean_expired after one second
    Then data will be cleared
    """
    nid ='id'
    cache.volatile_data[nid] = "test"
    cache.expiring[nid] = time.time() + 1
    cache.save_state()
    cache.volatile_data.clear()
    cache.load_state()
    assert cache.volatile_data[nid] ==  "test"
    del cache.volatile_data[nid]
    gevent.sleep(1)
    assert "id" not in cache.volatile_data



