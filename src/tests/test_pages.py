from unittest.mock import patch

import pytest

import bakesite.compile as compile


@pytest.fixture
def mock_fwrite():
    with patch("bakesite.compile.fwrite", autospec=True) as mock:
        yield mock


@pytest.fixture
def mock_glob():
    with patch("glob.glob", autospec=True) as mock:
        yield mock


class TestPages:
    def test_returns_no_date_in_page_when_not_existant_in_name(
        self, mock_glob, mock_fread, mock_fwrite
    ):
        mock_glob.return_value = ["/content/blog/Getting-Started.md"]
        mock_fread.return_value = "Here are some examples of how to write markdown."
        dst = "./_site/blog/{slug}/index.html"

        compile.make_pages("/content/blog", dst, template="post.html")

        args = mock_fwrite.call_args_list[0][0]
        assert args[0] == "./_site/blog/Getting-Started/index.html"
        assert "<p>Here are some examples of how to write markdown.</p>" in args[1]

    def test_returns_date_in_page_when_filename_contains_date(
        self, mock_glob, mock_fread, mock_fwrite
    ):
        mock_glob.return_value = ["/content/blog/2025-01-31-Getting-Started.md"]
        mock_fread.return_value = "Here are some examples of how to write markdown."
        src_dir = "./content/blog/*.md"
        dst = "./_site/blog/{slug}/index.html"

        compile.make_pages(src_dir, dst, template="post.html")

        args = mock_fwrite.call_args_list[0][0]
        assert args[0] == "./_site/blog/Getting-Started/index.html"
        assert "<p>Here are some examples of how to write markdown.</p>" in args[1]
        assert "2025-01-31" in args[1]

    def test_returns_pages_when_rendered(self, mock_glob, mock_fread, mock_fwrite):
        mock_glob.return_value = [
            "/content/blog/2025-01-31-Getting-Started.md",
            "/content/blog/2018-02-14-Another-Post.md",
        ]
        mock_fread.side_effect = [
            "Here are some examples of how to write markdown.",
            "Here are some examples of how to write markdown.",
        ]

        src_dir = "./content/blog/*.md"
        dst = "./_site/blog/{slug}/index.html"

        posts = compile.make_pages(src_dir, dst, template="post.html")

        assert len(posts) == 2
        assert posts[0]["date"] == "2025-01-31"
        assert posts[1]["date"] == "2018-02-14"

    def test_headers_params_are_not_reused_in_posts(
        self, mock_glob, mock_fread, mock_fwrite
    ):
        mock_glob.return_value = [
            "/content/blog/header-foo.md",
            "/content/blog/header-bar.md",
        ]
        mock_fread.side_effect = [
            "---\ntitle: Foo\ntags:\n- foo\n---\nFoo",
            "---\ntitle: Bar\ntags:\n- bar\n---\nBar",
        ]
        src = "./content/blog/*.md"
        dst = "./_site/{slug}/index.html"

        posts = compile.make_pages(src, dst, template="post.html")

        assert posts[0]["title"] == "Foo"
        assert posts[0]["tags"] == ["foo"]
        assert posts[1]["title"] == "Bar"
        assert posts[1]["tags"] == ["bar"]

    def test_content_rendering_enabled_when_defined_via_kwargs(
        self, mock_glob, mock_fread, mock_fwrite
    ):
        mock_glob.return_value = ["/content/blog/Getting-Started.md"]
        mock_fread.return_value = "foo:{{ author }}:Foo"
        src = "./content/blog/*.md"
        dst = "./_site/blog/{slug}/index.html"

        compile.make_pages(src, dst, template="post.html", author="Admin", render="yes")

        args = mock_fwrite.call_args_list[0][0]
        assert args[0] == "./_site/blog/Getting-Started/index.html"
        assert "<p>foo:Admin:Foo</p>" in args[1]

    def test_content_rendering_enabled_when_defined_in_headers(
        self, mock_glob, mock_fread, mock_fwrite
    ):
        mock_glob.return_value = ["/content/blog/Getting-Started.md"]
        mock_fread.return_value = "---\nrender: true\n---\nfoo:{{ author }}:Foo"
        src = "./content/blog/*.md"
        dst = "./_site/blog/{slug}/index.html"

        compile.make_pages(src, dst, template="post.html", author="Admin")

        args = mock_fwrite.call_args_list[0][0]
        assert args[0] == "./_site/blog/Getting-Started/index.html"
        assert "\n<p>foo:Admin:Foo</p>" in args[1]
