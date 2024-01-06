import os
import logging

def initialize_logging():

    log_file = os.path.join('Logs/logs.txt')

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )