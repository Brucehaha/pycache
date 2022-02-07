import os
import time
import pytest
import gevent
import tempfile
from pathlib import Path
from unittest.mock import patch


from src.cache import cache
from src.commands import set_expire_command, set_command, get_command

tmp_path = Path(tempfile.mkdtemp()) / "snapshot.rdb"


@pytest.fixture(autouse=True)
def run_before_and_after_tests(tmpdir):
    """Fixture to execute asserts before and after a test is run"""
    # Setup: fill with any logic you want

    yield # this is where the testing happens
    try:
        os.remove(tmp_path)
    except OSError:
        pass


@patch('src.cache.DB_PATH',tmp_path)
def test_save_and_load_state_succeed():
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


@patch('src.cache.DB_PATH',tmp_path)
def test_cache_expired_and_removed_succeed():
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



@patch('src.cache.DB_PATH',tmp_path)
def test_cache_expired_and_removed_succeed():
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

@patch('src.cache.DB_PATH',tmp_path)
def test_set_expire_command():
    """
    Given when store data in to cache with exipred time in 1 second
    When clean_expired after one second
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


@patch('src.cache.DB_PATH',tmp_path)
def test_set_expire_command():
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


@patch('src.cache.DB_PATH',tmp_path)
def test_set_command():
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

