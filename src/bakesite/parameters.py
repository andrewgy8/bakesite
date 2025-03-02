import logging

import click
import yaml

logger = logging.getLogger(__name__)


def load():
    try:
        stream = open("bakesite.yaml", "r")
    except FileNotFoundError:
        raise FileNotFoundError(
            "bakesite.yaml file not found. Please add one to the project."
        )
    params = yaml.safe_load(stream)
    click.echo(f"Baking site with parameters: {params}")
    return params
