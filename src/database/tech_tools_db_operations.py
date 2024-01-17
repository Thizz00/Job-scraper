import logging
from src.config.db_logs import log_collection
from src.logs_configure.mongodb_logs import create_log_entryTechTools
from src.models.tech_tools import TechTools
from src.database.database_initializer import handle_database_error

def add_data_to_database(session, df):
    try:
        for _, row in df.iterrows():
            new_job_offer = create_job_offer_instance(row)
            existing_offer = session.query(TechTools).filter_by(link=new_job_offer.link).first()

            if existing_offer:
                update_existing_offer(existing_offer, new_job_offer)
                logging.info(f"Updated existing job offer in the database: {existing_offer.link}")
                log_entry = create_log_entryTechTools(existing_offer)
                log_collection.insert_one(log_entry)

            else:
                session.add(new_job_offer)
                logging.info(f"Inserted new job offer into the database: {new_job_offer.link}")
                log_entry = create_log_entryTechTools(new_job_offer)
                log_collection.insert_one(log_entry)

        session.commit()
    except Exception as e:
        handle_database_error(e)
        session.rollback()
    finally:
        session.close()

def create_job_offer_instance(row):
    return TechTools(
        link=row['link'][0],
        tech_stack=row['tech_stack'],
        matched=row['matched']
    )

def update_existing_offer(existing_offer, new_job_offer):
    columns_to_update = ['tech_stack', 'matched']

    for column in columns_to_update:
        existing_value = getattr(existing_offer, column)
        new_value = getattr(new_job_offer, column)

        if existing_value != new_value:
            setattr(existing_offer, column, new_value)