import logging
import os

import click
import yaml

logger = logging.getLogger(__name__)


def load(project_path="."):
    try:
        for ext in (".yaml", ".yml"):
            file_path = project_path + "/bakesite" + ext
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    settings = yaml.safe_load(file)
                    click.echo(f"Baking site with parameters: {settings}")
                    return settings
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        raise FileNotFoundError(
            "bakesite.yaml file not found. Please add one to the project."
        )
