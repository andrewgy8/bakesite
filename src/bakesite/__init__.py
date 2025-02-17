import logging
import sys

import click

from bakesite import boilerplate, compile, parameters, server
from bakesite.logging import *  # noqa: F401 F403

logger = logging.getLogger(__name__)


@click.group()
def main():
    """Bakesite. The Simplest Static Site Generator."""
    pass


@main.command()
def init():
    """Initialize a new site"""
    boilerplate.initialize_project()


def _bake():
    try:
        params = parameters.load()
    except ImportError:
        click.echo(
            "settings.py file not found. Please add one to the project.", err=True
        )
        sys.exit(1)
    except AttributeError:
        click.echo("settings.py file does not contain a params dictionary.", err=True)
        sys.exit(1)
    compile.bake(params=params)


@main.command()
def bake():
    """Bake your markdown files into a static site"""
    _bake()


@main.command(help=f"Locally serve the site at http://localhost:{server.DEFAULT_PORT}")
@click.option(
    "--port",
    default=server.DEFAULT_PORT,
    help=f"Port to serve the site on. Default is {server.DEFAULT_PORT}.",
)
@click.option(
    "--bake",
    "do_bake",
    is_flag=True,
    default=False,
    help="Bake the site before serving.",
)
def serve(port, do_bake):
    if do_bake:
        _bake()
    server.serve(port)


if __name__ == "__main__":
    main()
