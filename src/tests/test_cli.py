import os
from click.testing import CliRunner
from bakesite import bake


class TestBake:
    def test_compiles_site(self, tmp_content_dir):
        runner = CliRunner()
        runner.invoke(bake)

        assert os.path.isdir("./_site")
