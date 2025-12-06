import logging
import sys
from typing import Any

# Configure Standard Logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

class AppLogger:
    """
    Standardized Application Logger
    Enforces clean logging practices.
    """
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)

    def info(self, msg: str, *args: Any, **kwargs: Any):
        self.logger.info(msg, *args, **kwargs)

    def debug(self, msg: str, *args: Any, **kwargs: Any):
        self.logger.debug(msg, *args, **kwargs)

    def warn(self, msg: str, *args: Any, **kwargs: Any):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args: Any, **kwargs: Any):
        self.logger.error(msg, *args, **kwargs)

def get_logger(name: str) -> AppLogger:
    return AppLogger(name)
