import tempfile
import shutil
import os

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
        list_layout = "<div>{{ content }}</div>"
        item_layout = "<p>{{ content }}</p>"
        compile.make_list(posts, dst, list_layout, item_layout)

        with open(os.path.join(tmp_site, "list.txt")) as f:
            assert f.read() == "<div><p>Foo</p><p>Bar</p></div>"

    def test_list_params(self, tmp_site):
        posts = [{"content": "Foo", "title": "foo"}, {"content": "Bar", "title": "bar"}]
        dst = os.path.join(tmp_site, "list.txt")
        list_layout = "<div>{{ key }}:{{ title }}:{{ content }}</div>"
        item_layout = "<p>{{ key }}:{{ title }}:{{ content }}</p>"
        compile.make_list(
            posts, dst, list_layout, item_layout, key="val", title="lorem"
        )
        with open(os.path.join(tmp_site, "list.txt")) as f:
            text = f.read()

        assert text == "<div>val:lorem:<p>val:foo:Foo</p><p>val:bar:Bar</p></div>"

    def test_dst_params(self, tmp_site):
        posts = [{"content": "Foo"}, {"content": "Bar"}]
        dst = os.path.join(tmp_site, "{{ key }}.txt")
        list_layout = "<div>{{ content }}</div>"
        item_layout = "<p>{{ content }}</p>"
        compile.make_list(posts, dst, list_layout, item_layout, key="val")

        expected_path = os.path.join(tmp_site, "val.txt")
        
        assert os.path.isfile(expected_path)
        with open(expected_path) as f:
            assert f.read() == "<div><p>Foo</p><p>Bar</p></div>"
