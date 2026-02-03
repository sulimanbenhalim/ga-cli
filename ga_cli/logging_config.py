"""Logging configuration for ga-cli"""

import logging
from pathlib import Path


def setup_logging():
    """Configure logging for ga-cli"""
    log_dir = Path.home() / '.ga-cli'
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / 'ga-cli.log'

    # Create logger
    logger = logging.getLogger('ga_cli')
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # File handler
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)

    # Console handler (only WARNING and above)
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


# Get logger singleton
logger = setup_logging()
