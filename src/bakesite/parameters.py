import logging
import os
import sys

import click

logger = logging.getLogger(__name__)


def load():
    sys.path.insert(0, os.getcwd())

    import settings

    params = settings.params
    click.echo(f"Baking site with parameters: {params}")
    return params
