import logging

def initialize_logging():
    import os
    import sys

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    log_file = os.path.join('logs/logs.txt')

    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,  # Change this to logging.DEBUG for detailed logs
        format='%(asctime)s - %(levelname)s - %(message)s'
    )