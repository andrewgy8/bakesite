import os
import tempfile


def temppath(*paths):
    return os.path.join(tempfile.gettempdir(), *paths)
