import logging
import sys


def get_logger(name):
    logger = logging.getLogger(name)
    logging.basicConfig(
        level=logging.INFO,
        # format="%(asctime)s [%(levelname)s] %(message)s",
        format="[%(levelname)s] %(message)s",
        handlers=[
            # logging.FileHandler("debug.log"),
            logging.StreamHandler(sys.stdout)
        ],
    )
    return logger
