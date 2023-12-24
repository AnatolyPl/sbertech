import logging
import logging.config
from logging import Logger
import sys

LOG_FORMAT = "[%(asctime)s %(levelname)s %(filename)s:%(lineno)s %(threadName)s %(name)s] %(message)s"


def get_logger(name) -> Logger:
    logging.basicConfig(format=LOG_FORMAT)
    logger = logging.getLogger(name)
    stdout = logging.StreamHandler(stream=sys.stdout)
    stdout.setLevel(logging.INFO)
    logger.addHandler(stdout)
    logger.setLevel(logging.INFO)

    return logger
