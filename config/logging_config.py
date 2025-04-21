import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
LOG_FILE = "app.log"

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)

LOG_FORMAT = (
    "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d - %(funcName)s()] %(message)s"
)

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        RotatingFileHandler(LOG_PATH, maxBytes=5*1024*1024,
                            backupCount=5),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("app_logger")
