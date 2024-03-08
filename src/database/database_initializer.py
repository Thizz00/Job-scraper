from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.db_data import Base, DATABASE_URL
from src.config.db_logs import log_collection

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.logs_configure.logger_config import configure_logger

logger = configure_logger()

def initialize_database():
    try:
        engine = create_engine(DATABASE_URL, echo=True)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        log_collection.insert_one({
        'level': 'info',
        'message': f"Connected to the database",
    })
        return engine, session
    except Exception as e:
        logger.error(f"Error connecting to the database: {str(e)}")
        log_collection.insert_one({
        'level': 'error',
        'message': f"Error connecting to the database: {str(e)}",
    })
        return None, None