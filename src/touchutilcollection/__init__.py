from td import *  # pyright: ignore[reportMissingImports]

__minimum_td_version__ = "2023.1200"

from importlib.metadata import version

__version__ = version("touchutilcollection")

import logging
from os import environ

logger = logging.getLogger()
log_level = getattr(logging, environ.get("TOUCHLAUNCH_LOGLEVEL", "INFO"), None) or logging.INFO
logging.basicConfig(level=log_level)

if float(app.build) < float(__minimum_td_version__):
    logger.warning(f"{__minimum_td_version__} required, found {app.build}")