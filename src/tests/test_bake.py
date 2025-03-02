import os

from bakesite import compile


class TestBake:
    def test_site_missing(self, mock_params, tmp_content_dir):
        compile.bake(mock_params)

    def test_site_exists(self, mock_params, tmp_path, tmp_content_dir):
        d = tmp_path / "_site"
        d.mkdir()
        f = d / "foo.txt"
        f.write_text("foo")

        compile.bake(mock_params)

        assert not os.path.isfile("_site/foo.txt")

    def test_default_params(self, mock_params, tmpdir, tmp_content_dir):
        compile.bake(mock_params, target_dir=str(tmpdir))

        with open(tmpdir / "blog/index.html") as f:
            s1 = f.read()

        with open(tmpdir / "blog/rss.xml") as f:
            s2 = f.read()

        assert '<a href="/">Home</a>' in s1

        assert "<title>Blog - AGY</title>" in s1

        assert "<link>https://test.grahamyooll.com/</link>" in s2
