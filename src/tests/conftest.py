import os
import shutil
from unittest.mock import patch
import pytest

from bakesite import compile


@pytest.fixture
def tmp_content_dir():
    shutil.copytree("./src/bakesite/boilerplate", ".", dirs_exist_ok=True)
    yield
    shutil.rmtree("./content")
    os.remove("./settings.py")


@pytest.fixture
def mock_fread():
    with patch.object(compile, "fread") as mock:
        yield mock
