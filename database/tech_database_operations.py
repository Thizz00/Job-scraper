import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.db_data import Base, DATABASE_URL
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
            existing_offer = session.query(TechTools).filter_by(link=new_job_offer.link).first()
            
            if existing_offer:
                update_existing_offer(existing_offer, new_job_offer)
            else:
                session.add(new_job_offer)
                logging.info(f"Inserted new job offer into the database: {new_job_offer.link}")
                log_entry = create_log_entry(new_job_offer)
                log_collection.insert_one(log_entry)
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

def update_existing_offer(existing_offer, new_job_offer):
    columns_to_update = [
        'tech_stack','matched'
    ]

    for column in columns_to_update:
        setattr(existing_offer, column, getattr(new_job_offer, column))

    logging.info(f"Updated existing job offer in the database: {existing_offer.link}")
    log_entry = create_log_entry(existing_offer)
    log_collection.insert_one(log_entry)

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