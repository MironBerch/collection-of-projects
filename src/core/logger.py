import os
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('__main__')
logger.setLevel(logging.INFO)

try:
    os.mkdir('../logs')
except FileExistsError:
    ...


file_handler = RotatingFileHandler(
    '../logs/main.log',
    maxBytes=24*1024*1024,
    backupCount=10,
)
file_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
)

logger.addHandler(file_handler)
logger.addHandler(logging.StreamHandler())
