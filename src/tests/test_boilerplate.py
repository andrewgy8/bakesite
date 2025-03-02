import os
import shutil

import pytest

from bakesite import boilerplate


class TestBoilerplate:
    def teardown_method(self):
        if os.path.exists(f"{os.getcwd()}/content"):
            shutil.rmtree(f"{os.getcwd()}/content")

        if os.path.exists(f"{os.getcwd()}/bakesite.yaml"):
            os.remove(f"{os.getcwd()}/bakesite.yaml")

    def test_returns_copy_of_boilerplate_when_does_not_exist(self):
        with pytest.raises(SystemExit) as exit:
            boilerplate.initialize_project()

        assert os.path.exists(f"{os.getcwd()}/content")
        assert os.path.exists(f"{os.getcwd()}/bakesite.yaml")
        assert exit.value.code == 0

    def test_exits_when_content_directory_exists(self):
        os.mkdir(f"{os.getcwd()}/content")

        with pytest.raises(SystemExit) as exit:
            boilerplate.initialize_project()

        assert exit.value.code == 1

    def test_exits_when_settings_file_exists(self):
        with open(f"{os.getcwd()}/bakesite.yaml", "w") as f:
            f.write("")

        with pytest.raises(SystemExit) as exit:
            boilerplate.initialize_project()

        assert exit.value.code == 1
