from bakesite import parameters


class TestLoad:
    def test_returns_dict_of_settings_file_values(self, tmp_content_dir):
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
