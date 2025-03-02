import bakesite.compile as compile


class TestRender:
    def test_oneline_template(self):
        tpl = "{slug}.md"
        out = compile.format_file_path(tpl, slug="bar")

        assert out == "bar.md"
