import logging
import os
import sys

logger = logging.getLogger(__name__)


def load():
    sys.path.insert(0, os.getcwd())

    import settings

    params = settings.params
    logger.info(f"Baking site with parameters: {params}")
    return params
