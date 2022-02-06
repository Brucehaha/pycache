import os
import tempfile
from pathlib import Path

from unittest.mock import patch


from src.cache import cache



tmp_path = Path(tempfile.mkdtemp()) / "snapshot.rdb"

@patch('src.settings.DB_PATH',)
def test_save_and_load_state_succeed(db_path):
    cache.volatile_data['id'] = 1
    cache.volatile_data['message'] = "hello world"
    cache.save_sate()
    assert os.path.exists(db_path)
    cache.volatile_data.clear()
    cache.load_state()
    assert cache.volatile_data['id'] == 1
    assert cache.volatile_data['message'] == "hello world"
