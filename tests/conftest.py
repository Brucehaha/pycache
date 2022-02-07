import os
import pytest
import tempfile
from pathlib import Path
from typing import Iterator
from unittest.mock import patch


from src.cache import cache

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

@pytest.fixture(scope="session", autouse=True)
def default_temp_path() -> Iterator[None]:
    with patch("src.cache.DB_PATH"):
        yield



@pytest.fixture(scope="session",)
def default_temp_path() -> Iterator[None]:
    return tmp_path