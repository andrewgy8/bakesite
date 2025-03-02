from datetime import date
import bakesite.compile as compile


class TestHeaders:
    def test_returns_only_a_single_header(self):
        text = """---
title: Groupthink In Engineering Teams
---"""
        headers = compile.read_headers(text)

        assert headers == {"title": "Groupthink In Engineering Teams"}

    def test_returns_only_multiple_headers(self):
        text = """---
title: Groupthink In Engineering Teams
tags:
    - Engineering
    - Teamwork
render: true
edited on: 2025-02-28
---"""
        headers = compile.read_headers(text)

        assert headers == {
            "title": "Groupthink In Engineering Teams",
            "tags": ["Engineering", "Teamwork"],
            "render": True,
            "edited on": date(2025, 2, 28),
        }

    def test_returns_only_headers_when_text_exists(self):
        text = """---
title: Groupthink In Engineering Teams
tags:
    - Engineering
    - Teamwork
render: true
edited on: 2025-02-28
---

# What is Groupthink?"""

        headers = compile.read_headers(text)

        assert headers == {
            "title": "Groupthink In Engineering Teams",
            "tags": ["Engineering", "Teamwork"],
            "render": True,
            "edited on": date(2025, 2, 28),
        }

    def test_returns_empty_dict_when_no_headers(self):
        text = "# What is Groupthink?"
        headers = compile.read_headers(text)

        assert headers == {}

    def test_returns_empty_dict_when_no_content(self):
        text = ""
        headers = compile.read_headers(text)

        assert headers == {}
