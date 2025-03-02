import os
import shutil
import sys

import click


def _does_project_exist():
    if os.path.exists(f"{os.getcwd()}/content"):
        click.echo(
            "Project already initialized since we detect you have a content directory.",
            err=True,
        )
        sys.exit(1)
    elif os.path.exists(f"{os.getcwd()}/bakesite.yaml"):
        click.echo(
            "Project already initialized since we detect you have bakesite.yaml file.",
            err=True,
        )
        sys.exit(1)
    return False


def initialize_project():
    _does_project_exist()

    try:
        shutil.copytree(
            f"{os.path.dirname(__file__)}/boilerplate/", os.getcwd(), dirs_exist_ok=True
        )
        click.echo(
            "Project initialized successfully. Please run 'bakesite bake' to generate the site."
        )
        sys.exit(0)
    except FileExistsError:
        click.echo("Project already initialized.", err=True)
        sys.exit(1)
