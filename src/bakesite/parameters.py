import logging
import os
import sys

logger = logging.getLogger(__name__)


def load():
    sys.path.insert(
        0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    )

    import settings

    params = settings.params
    logger.info(f"Baking site with parameters: {params}")
    return params
