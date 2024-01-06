from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.db_data import Base, DATABASE_URL
from config.db_logs import log_collection
import logging

def initialize_database():
    try:
        engine = create_engine(DATABASE_URL, echo=True)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        return engine, session
    except Exception as e:
        handle_database_error(e)
        return None, None
    
def handle_database_error(error):
    logging.error(f"Error connecting to the database: {str(error)}")
    log_collection.insert_one({
        'level': 'error',
        'message': f"Error connecting to the database: {str(error)}",
    })
