from bakesite import compile


class TestContent:
    def test_content_content(self, mock_fread):
        mock_fread.return_value = "hello world"

        content = compile.read_content("somefile.md")

        assert content["content"] == "<p>hello world</p>\n"

    def test_content_date(self, mock_fread):
        mock_fread.return_value = "hello world"

        content = compile.read_content("2018-01-01-foo.md")

        assert content["date"] == "2018-01-01"
        assert content["slug"] == "foo"

    def test_content_date_missing(self, mock_fread):
        mock_fread.return_value = "hello world"

        content = compile.read_content("foo.md")

        assert content["date"] == "1970-01-01"
        assert content["slug"] == "foo"

    def test_content_headers(self, mock_fread):
        mock_fread.return_value = "<!-- a: 1 -->\n<!-- b: 2 -->\nFoo"

        content = compile.read_content("foo.md")

        assert content["a"] == "1"
        assert content["b"] == "2"
        assert content["content"] == "<p>Foo</p>\n"
