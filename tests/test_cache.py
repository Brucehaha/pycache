import os

from src.cache import cache


def test_save_and_load_state_succeed():
    cache.volatile_data['id'] = 1
    cache.volatile_data['message'] = "hello world"
    cache.save_sate()
    assert os.path.exists("path_to_rdb")
    cache.volatile_data.clear()
    cache.load_state()
    assert cache.volatile_data['id'] == 1
    assert cache.volatile_data['message'] == "hello world"
