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
    if os.path.exists("./bakesite.yaml"):
        os.remove("./bakesite.yaml")


@pytest.fixture
def mock_fread():
    with patch.object(compile, "fread") as mock:
        yield mock


@pytest.fixture
def mock_params():
    return {
        "base_path": "",
        "subtitle": "AGY",
        "author": "Andrew Graham-Yooll",
        "site_url": "https://test.grahamyooll.com",
        "current_year": 2002,
        "github_url": "https://github.com/andrewgy8",
        "linkedin_url": "https://www.linkedin.com",
        "gtag_id": "G-1234",
        "cname": "test.grahamyooll.com",
    }
