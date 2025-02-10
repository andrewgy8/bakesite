import bakesite.compile as compile


class TestRFC822Date:
    def test_epoch(self):
        assert (
            compile.rfc_2822_format("1970-01-01") == "Thu, 01 Jan 1970 00:00:00 +0000"
        )

    def test_2018_06_16(self):
        assert (
            compile.rfc_2822_format("2018-06-16") == "Sat, 16 Jun 2018 00:00:00 +0000"
        )
