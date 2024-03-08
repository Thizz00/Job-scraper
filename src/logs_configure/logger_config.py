import logging
from logging.handlers import TimedRotatingFileHandler

def configure_logger():
    import os
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    log_dir = 'Logs'
    os.makedirs(log_dir, exist_ok=True)

    log_file_path = os.path.join(log_dir, "logs.log")

    handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1, backupCount=3)
    handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s'))

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger