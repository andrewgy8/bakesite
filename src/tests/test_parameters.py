import os

import pytest
from bakesite import parameters


class TestLoad:
    def test_returns_dict_of_configuration_file_values(self, tmp_content_dir):
        settings = parameters.load()

        assert settings == {
            "base_path": "",
            "subtitle": "<Your subtitle here>",
            "author": "<Your name here>",
            "site_url": "https://<your site here>.com",
            "current_year": 2025,
            "github_url": "https://github.com/<your github here>",
            "linkedin_url": "https://www.linkedin.com/<your linkedin here>",
            "gtag_id": "<Your gtag here>",
            "cname": "<your CNAME here>",
        }

    def test_returns_dict_of_configuration_values_when_yml_extension(
        self, tmp_content_dir
    ):
        os.rename("bakesite.yaml", "bakesite.yml")

        settings = parameters.load()

        assert settings == {
            "base_path": "",
            "subtitle": "<Your subtitle here>",
            "author": "<Your name here>",
            "site_url": "https://<your site here>.com",
            "current_year": 2025,
            "github_url": "https://github.com/<your github here>",
            "linkedin_url": "https://www.linkedin.com/<your linkedin here>",
            "gtag_id": "<Your gtag here>",
            "cname": "<your CNAME here>",
        }

        os.remove("bakesite.yml")

    def test_raises_file_not_found_error_when_no_configuration_file(
        self, tmp_content_dir
    ):
        os.remove("bakesite.yaml")

        with pytest.raises(FileNotFoundError) as exc:
            parameters.load()

        assert (
            str(exc.value)
            == "bakesite.yaml file not found. Please add one to the project."
        )
