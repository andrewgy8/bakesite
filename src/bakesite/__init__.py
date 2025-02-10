import argparse
import logging
from math import log
import sys

from bakesite.logging import *  # noqa: F401 F403

from bakesite import boilerplate, parameters
from bakesite.compile import bake
from bakesite.server import serve


logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        prog="Bakesite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Bakesite. \nThe Simplest Static Site Generator.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("init", help="initialize a new site")
    subparsers.add_parser("bake", help="bake your markdown files into a static site")
    subparsers.add_parser(
        "serve", help="locally serve the site at http://localhost:8003"
    )
    args = parser.parse_args()
    if args.command == "init":
        boilerplate.initialize_project()

    try:
        params = parameters.load()
    except ImportError:
        logger.error("settings.py file not found. Please add one to the project.")
        sys.exit(1)
    except AttributeError:
        logger.error("settings.py file does not contain a params dictionary.")
        sys.exit(1)

    if args.command == "bake":
        bake(params=params)
    elif args.command == "serve":
        serve()
