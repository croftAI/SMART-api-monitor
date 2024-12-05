import logging
import sys
from typing import Optional
from datetime import datetime


class Logger:
    def __init__(self, name: str, level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level))

        if not self.logger.handlers:
            self._setup_handlers()

    def _setup_handlers(self):
        # Console handler
        console = logging.StreamHandler(sys.stdout)
        console.setFormatter(self._get_formatter())
        self.logger.addHandler(console)

        # File handler
        file_handler = logging.FileHandler(
            f"logs/{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler.setFormatter(self._get_formatter())
        self.logger.addHandler(file_handler)

    def _get_formatter(self):
        return logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )


def get_logger(name: str, level: str = "INFO") -> Logger:
    return Logger(name, level)