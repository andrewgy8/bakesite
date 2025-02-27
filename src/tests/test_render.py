import bakesite.compile as compile


class TestRender:
    def test_oneline_template(self):
        tpl = "foo {{ key1 }} baz {{ key2 }}"
        out = compile.rename_file_with_slug(tpl, key1="bar", key2="qux")

        assert out == "foo bar baz qux"

    def test_multiline_template(self):
        tpl = "foo {{ key1 }}\nbaz {{ key1 }}"
        out = compile.rename_file_with_slug(tpl, key1="bar")

        assert out == "foo bar\nbaz bar"

    def test_repeated_key(self):
        tpl = "foo {{ key1 }} baz {{ key1 }}"
        out = compile.rename_file_with_slug(tpl, key1="bar")

        assert out == "foo bar baz bar"

    def test_multiline_placeholder(self):
        tpl = "foo {{\nkey1\n}} baz {{\nkey2\n}}"
        out = compile.rename_file_with_slug(tpl, key1="bar", key2="qux")

        assert out == "foo bar baz qux"
