import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('__main__')
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler(
    'main.log',
    maxBytes=48*1024*1024,
    backupCount=5,
)
file_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
)

logger.addHandler(file_handler)
logger.addHandler(logging.StreamHandler())
