import os
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


@pytest.mark.usefixtures("mock_fwrite")
class TestPages:
    def test_pages_undated(self, mock_glob, mock_fread, mock_fwrite):
        mock_glob.return_value = ["/content/blog/Getting-Started.md"]
        mock_fread.return_value = "Here are some examples of how to write markdown."
        dst = "./_site/blog/{{ slug }}/index.html"

        compile.make_pages("/content/blog", dst, template="post.html")

        args = mock_fwrite.call_args_list[0][0]
        assert args[0] == "./_site/blog/Getting-Started/index.html"
        assert "<p>Here are some examples of how to write markdown.</p>" in args[1]

    def test_pages_dated(self, mock_glob, mock_fread, mock_fwrite):
        mock_glob.return_value = ["/content/blog/2025-01-31-Getting-Started.md"]
        mock_fread.return_value = "Here are some examples of how to write markdown."
        src_dir = "./content/blog/*.md"
        dst = "./_site/blog/{{ slug }}/index.html"

        compile.make_pages(src_dir, dst, template="post.html")

        args = mock_fwrite.call_args_list[0][0]
        assert args[0] == "./_site/blog/Getting-Started/index.html"
        assert "<p>Here are some examples of how to write markdown.</p>" in args[1]
        assert "2025-01-31" in args[1]

    def test_pages_return_value(self):
        src_dir = "./content/blog/*.md"
        dst = "./_site/blog/{{ slug }}/index.html"

        posts = compile.make_pages(src_dir, dst, template="post.html")

        assert len(posts) == 2
        assert posts[0]["date"] == "2025-01-31"
        assert posts[1]["date"] == "2018-02-14"

    def test_content_header_params(self):
        # Test that header params from one post is not used in another
        # post.
        src = os.path.join(self.blog_path, "header*.txt")
        dst = os.path.join(self.site_path, "{{ slug }}.txt")
        tpl = "{{ title }}:{{ tag }}:{{ content }}"
        compile.make_pages(src, dst, tpl)
        with open(os.path.join(self.site_path, "header-foo.txt")) as f:
            assert f.read() == "{{ title }}:foo:Foo"
        with open(os.path.join(self.site_path, "header-bar.txt")) as f:
            assert f.read() == "bar:{{ tag }}:Bar"

    def test_content_no_rendering(self):
        # Test that placeholders are not populated in content rendering
        # by default.
        src = os.path.join(self.blog_path, "placeholder-foo.txt")
        dst = os.path.join(self.site_path, "{{ slug }}.txt")
        tpl = "<div>{{ content }}</div>"
        compile.make_pages(src, dst, tpl, author="Admin")

        with open(os.path.join(self.site_path, "placeholder-foo.txt")) as f:
            assert f.read() == "<div>{{ title }}:{{ author }}:Foo</div>"

    def test_content_rendering_via_kwargs(self):
        # Test that placeholders are populated in content rendering when
        # requested in make_pages.
        src = os.path.join(self.blog_path, "placeholder-foo.txt")
        dst = os.path.join(self.site_path, "{{ slug }}.txt")
        tpl = "<div>{{ content }}</div>"
        compile.make_pages(src, dst, tpl, author="Admin", render="yes")

        with open(os.path.join(self.site_path, "placeholder-foo.txt")) as f:
            assert f.read() == "<div>foo:Admin:Foo</div>"

    def test_content_rendering_via_header(self):
        # Test that placeholders are populated in content rendering when
        # requested in content header.
        src = os.path.join(self.blog_path, "placeholder-bar.txt")
        dst = os.path.join(self.site_path, "{{ slug }}.txt")
        tpl = "<div>{{ content }}</div>"
        compile.make_pages(src, dst, tpl, author="Admin")

        with open(os.path.join(self.site_path, "placeholder-bar.txt")) as f:
            assert f.read() == "<div>bar:Admin:Bar</div>"

    @pytest.mark.skip
    def test_rendered_content_in_summary(self):
        # Test that placeholders are populated in summary if and only if
        # content rendering is enabled.
        src = os.path.join(self.blog_path, "placeholder*.txt")
        post_dst = os.path.join(self.site_path, "{{ slug }}.txt")
        list_dst = os.path.join(self.site_path, "list.txt")
        post_layout = ""
        list_layout = "<div>{{ content }}</div>"
        item_layout = "<p>{{ summary }}</p>"
        posts = compile.make_pages(src, post_dst, post_layout, author="Admin")
        compile.make_list(posts, list_dst, list_layout, item_layout)

        with open(os.path.join(self.site_path, "list.txt")) as f:
            assert (
                f.read()
                == "<div><p>{{ title }}:{{ author }}:Foo</p><p>bar:Admin:Bar</p></div>"
            )
