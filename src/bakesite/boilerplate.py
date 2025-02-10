import os
import shutil
import logging
import sys


logger = logging.getLogger(__name__)


def _does_project_exist():
    if os.path.exists(f"{os.getcwd()}/content"):
        logger.error(
            "Project already initialized since we detect you have a content directory.",
        )
        sys.exit(1)
    elif os.path.exists(f"{os.getcwd()}/settings.py"):
        logger.error(
            "Project already initialized since we detect you have settings.py file.",
        )
        sys.exit(1)
    return False


def initialize_project():
    _does_project_exist()

    try:
        shutil.copytree(
            f"{os.path.dirname(__file__)}/boilerplate/", os.getcwd(), dirs_exist_ok=True
        )
        logger.info(
            "Project initialized successfully. Please run 'bakesite bake' to generate the site."
        )
        sys.exit(0)
    except FileExistsError:
        logger.error("Project already initialized.", exc_info=True)
        sys.exit(1)
