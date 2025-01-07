import logging
import os

def get_logger(name="default_logger"):
    """
    configure a simple logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(console_handler)

    return logger
