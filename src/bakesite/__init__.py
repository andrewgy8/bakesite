import logging
import sys

from bakesite.logging import *  # noqa: F401 F403

from bakesite import boilerplate, parameters
from bakesite import compile, server
import click


logger = logging.getLogger(__name__)


@click.group()
def main():
    """Bakesite. The Simplest Static Site Generator."""
    pass


@main.command()
def init():
    """Initialize a new site"""
    boilerplate.initialize_project()


@main.command()
def bake():
    """Bake your markdown files into a static site"""
    try:
        params = parameters.load()
    except ImportError:
        click.echo("settings.py file not found. Please add one to the project.", err=True)
        sys.exit(1)
    except AttributeError:
        click.echo("settings.py file does not contain a params dictionary.", err=True)
        sys.exit(1)
    compile.bake(params=params)


@main.command()
@click.option(
    "--port",
    default=server.PORT,
    help=f"Port to serve the site on. Default is {server.PORT}.",
)
def serve(port):
    """Locally serve the site at http://localhost:8003"""
    server.serve(port)


if __name__ == "__main__":
    main()
