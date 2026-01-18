import os
import shutil
import tempfile

import pytest

import bakesite.compile as compile


class TestCollectAllTags:
    def test_collects_tags_from_multiple_posts(self):
        posts = [
            {"title": "Post 1", "tags": ["python", "tutorial"]},
            {"title": "Post 2", "tags": ["python", "web"]},
            {"title": "Post 3", "tags": ["javascript"]},
        ]
        result = compile.collect_all_tags(posts)
        assert result == ["javascript", "python", "tutorial", "web"]

    def test_handles_posts_without_tags(self):
        posts = [
            {"title": "Post 1", "tags": ["python"]},
            {"title": "Post 2"},  # No tags
            {"title": "Post 3", "tags": []},  # Empty tags
        ]
        result = compile.collect_all_tags(posts)
        assert result == ["python"]

    def test_handles_string_tags(self):
        posts = [
            {"title": "Post 1", "tags": "single-tag"},
        ]
        result = compile.collect_all_tags(posts)
        assert result == ["single-tag"]

    def test_returns_sorted_tags(self):
        posts = [
            {"title": "Post 1", "tags": ["zebra", "apple", "mango"]},
        ]
        result = compile.collect_all_tags(posts)
        assert result == ["apple", "mango", "zebra"]

    def test_empty_posts_returns_empty_list(self):
        result = compile.collect_all_tags([])
        assert result == []


@pytest.fixture
def tmp_site():
    path = os.path.join(tempfile.gettempdir(), "tag_site")
    yield path
    if os.path.exists(path):
        shutil.rmtree(path)


class TestMakeTagPages:
    def test_creates_tag_pages(self, tmp_site):
        posts = [
            {"title": "Post 1", "content": "Content 1", "tags": ["python"]},
            {"title": "Post 2", "content": "Content 2", "tags": ["python", "web"]},
        ]
        all_tags = ["python", "web"]

        compile.make_tag_pages(posts, tmp_site, "blog", all_tags)

        # Check python tag page exists
        python_page = os.path.join(tmp_site, "blog", "tag", "python", "index.html")
        assert os.path.isfile(python_page)

        # Check web tag page exists
        web_page = os.path.join(tmp_site, "blog", "tag", "web", "index.html")
        assert os.path.isfile(web_page)

    def test_tag_page_contains_correct_posts(self, tmp_site):
        posts = [
            {"title": "Python Post", "content": "Python content", "tags": ["python"]},
            {"title": "Web Post", "content": "Web content", "tags": ["web"]},
        ]
        all_tags = ["python", "web"]

        compile.make_tag_pages(posts, tmp_site, "blog", all_tags)

        # Python page should only have Python Post
        python_page = os.path.join(tmp_site, "blog", "tag", "python", "index.html")
        with open(python_page) as f:
            content = f.read()
            assert "Python Post" in content
            assert "Web Post" not in content
