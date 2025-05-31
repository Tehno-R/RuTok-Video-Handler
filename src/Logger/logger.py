import logging
import sys

file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.INFO)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)

DEG_MS = '05'

strfmt = f'[%(asctime)s.%(msecs){DEG_MS}d] [%(name)s] [%(levelname)s] %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(fmt=strfmt, datefmt=datefmt)
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

def generate_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger
