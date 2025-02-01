import bakesite.compile as compile


class TestHeader:
    def test_single_header(self):
        text = "<!-- key1: val1 -->"
        headers = list(compile.read_headers(text))
        assert headers == [("key1", "val1", 19)]

    def test_multiple_headers(self):
        text = "<!-- key1: val1 -->\n<!-- key2: val2-->"
        headers = list(compile.read_headers(text))
        assert headers == [("key1", "val1", 20), ("key2", "val2", 38)]

    def test_headers_and_text(self):
        text = "<!-- a: 1 -->\n<!-- b: 2 -->\nFoo\n<!-- c: 3 -->"
        headers = list(compile.read_headers(text))
        assert headers == [("a", "1", 14), ("b", "2", 28)]

    def test_headers_and_blank_line(self):
        text = "<!-- a: 1 -->\n<!-- b: 2 -->\n\n<!-- c: 3 -->\n"
        headers = list(compile.read_headers(text))
        assert headers == [("a", "1", 14), ("b", "2", 29), ("c", "3", 43)]

    def test_multiline_header(self):
        text = "<!--\na: 1 --><!-- b:\n2 -->\n<!-- c: 3\n-->"
        headers = list(compile.read_headers(text))
        assert headers == [("a", "1", 13), ("b", "2", 27), ("c", "3", 40)]

    def test_no_header(self):
        headers = list(compile.read_headers("Foo"))
        assert headers == []

    def test_empty_string(self):
        headers = list(compile.read_headers(""))
        assert headers == []
