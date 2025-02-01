import os
import shutil

import bakesite.compile as compile
from tests import path


class TestFileIO:
    def test_fread(self):
        text = "foo\nbar\n"
        filepath = path.temppath("foo.txt")
        with open(filepath, "w") as f:
            f.write(text)
        text_read = compile.fread(filepath)
        os.remove(filepath)

        assert text_read == text

    def test_fwrite(self):
        text = "baz\nqux\n"
        filepath = path.temppath("foo.txt")
        compile.fwrite(filepath, text)
        with open(filepath) as f:
            text_read = f.read()
        os.remove(filepath)

        assert text_read == text

    def test_fwrite_makedir(self):
        text = "baz\nqux\n"
        dirpath = path.temppath("foo", "bar")
        filepath = os.path.join(dirpath, "foo.txt")
        compile.fwrite(filepath, text)
        with open(filepath) as f:
            text_read = f.read()
        assert os.path.isdir(dirpath)
        shutil.rmtree(path.temppath("foo"))

        assert text_read == text
