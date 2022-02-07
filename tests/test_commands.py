import gevent

from src.cache import cache
from src.commands import set_expire_command, set_command, get_command, flush_command

def test_set_expire_command(tmp_path):
    """
    Given when store data in to cache with exipred time in 1 second
    When run set_expire_command after one second
    Then data will be cleared
    """
    nid ='id'
    cache.volatile_data[nid] = "test"
    cache.save_state()
    assert cache.volatile_data[nid] ==  "test"
    set_expire_command(nid,1)
    assert nid in cache.expiring
    gevent.sleep(1)
    assert "id" not in cache.volatile_data
    assert nid not in cache.expiring


def test_set_get_flush_command(tmp_path):
    """
    Set command
    """
    nid ='test_id'
    set_command(nid, 'test')
    assert cache.volatile_data[nid] ==  "test"

    del cache.volatile_data[nid]
    assert nid not in cache.volatile_data

    cache.load_state()
    assert nid in cache.volatile_data

    _, value = get_command(nid)
    assert value == cache.volatile_data[nid]

    flush_command()

    assert value not in cache.volatile_data
    cache.load_state()
    assert value not in cache.volatile_data



