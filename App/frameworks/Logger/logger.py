import logging

handler = logging.FileHandler('logs.log')
handler.setLevel(logging.INFO)

DEG_MS = '05'

strfmt = f'[%(asctime)s.%(msecs){DEG_MS}d] [%(name)s] [%(levelname)s] %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(fmt=strfmt, datefmt=datefmt)
handler.setFormatter(formatter)

def generate_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger
