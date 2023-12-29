import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.base import Base
from config.db_data import DATABASE_URL
from config.db_logs import log_collection
from models.tech_tools import TechTools

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

def add_data_to_database(session, df):
    try:
        for _, row in df.iterrows():
            new_job_offer = create_job_offer_instance(row)
            session.add(new_job_offer)
            logging.info(f"Inserted new job offer into the database: {
                             new_job_offer}")
            log_entry = create_log_entry(new_job_offer)
            log_collection.insert_one(log_entry)

        session.commit()
    except Exception as e:
        handle_database_error(e)
        session.rollback()
    finally:
        session.close()


def create_job_offer_instance(row):
    return TechTools(
        link = row['link'][0],
        tech_stack=row['tech_stack'],
        matched=row['matched']
    )

def create_log_entry(job_offer):
    entry = {'level': 'Success'}
    for column in TechTools.__table__.columns:
        entry[column.name] = str(getattr(job_offer, column.name))
    return entry


def handle_database_error(error):
    logging.error(f"Error connecting to the database: {str(error)}")
    log_collection.insert_one({
        'level': 'error',
        'message': f"Error connecting to the database: {str(error)}",
    })