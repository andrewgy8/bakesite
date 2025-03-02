import os
import shutil
import tempfile

import pytest

import bakesite.compile as compile


@pytest.fixture
def tmp_site():
    path = os.path.join(tempfile.gettempdir(), "site")
    yield path
    shutil.rmtree(path)


class TestList:
    def test_returns_list(self, tmp_site):
        posts = [{"content": "Foo"}, {"content": "Bar"}]
        dst = os.path.join(tmp_site, "list.txt")

        compile.make_list(posts, dst)

        with open(os.path.join(tmp_site, "list.txt")) as f:
            html = f.read()
            assert "Foo" in html
            assert "Bar" in html

    def test_list_params(self, tmp_site):
        posts = [
            {"content": "Foo", "title": "foo"},
            {"content": "Bar", "title": "bar"},
        ]
        dst = os.path.join(tmp_site, "list.txt")
        compile.make_list(posts, dst, key="val", title="lorem")
        with open(os.path.join(tmp_site, "list.txt")) as f:
            text = f.read()

        assert "Foo" in text
        assert "<h1>lorem</h1>" in text
        assert "Bar" in text

    def test_dst_params(self, tmp_site):
        posts = [{"content": "Foo"}, {"content": "Bar"}]
        dst = os.path.join(tmp_site, "{key}.md")

        compile.make_list(posts, dst, key="val")

        expected_path = os.path.join(tmp_site, "val.md")

        assert os.path.isfile(expected_path)
        with open(expected_path) as f:
            assert '<p class="summary">\n    Foo' in f.read()
