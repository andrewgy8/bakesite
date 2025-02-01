import pytest
from bakesite import compile
import os


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


@pytest.mark.xfail
class TestMain:
    def test_site_missing(self, mock_params):
        compile.bake(mock_params)

    def test_site_exists(self, mock_params, tmp_path):
        d = tmp_path / "_site"
        d.mkdir()
        f = d / "foo.txt"
        f.write_text("foo")

        compile.bake(mock_params)

        assert not os.path.isfile("_site/foo.txt")

    def test_default_params(self, mock_params, tmpdir):
        compile.bake(mock_params, target_dir=tmpdir)

        with open(tmpdir / "blog/index.html") as f:
            s1 = f.read()

        with open(tmpdir / "blog/rss.xml") as f:
            s2 = f.read()

        assert '<a href="/">Home</a>' in s1

        assert "<title>Blog - AGY</title>" in s1

        assert "<link>https://test.grahamyooll.com/</link>" in s2
