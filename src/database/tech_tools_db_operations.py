from src.config.db_logs import log_collection
from src.models.tech_tools import TechTools
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.logs_configure.logger_config import configure_logger

logger = configure_logger()



def add_data_to_database(session, df):
    try:
        for _, row in df.iterrows():
            new_job_offer = create_job_offer_instance(row)
            existing_offer = session.query(TechTools).filter_by(link=new_job_offer.link).first()

            if existing_offer:
                update_existing_offer(existing_offer, new_job_offer)
                logger.info(f"Updated existing job offer in the database: {existing_offer.link}")
                log_collection.insert_one({
                    'level': 'info',
                    'message': f"Updated existing job offer in the database: {existing_offer.link}",
                })

            else:
                session.add(new_job_offer)
                logger.info(f"Inserted new job offer into the database: {new_job_offer.link}")
                log_collection.insert_one({
                    'level': 'info',
                    'message': f"Inserted new job offer into the database: {new_job_offer.link}",
                })

        session.commit()
    except Exception as e:
        logger.error(f"Error connecting to the database: {str(e)}")
        log_collection.insert_one({
        'level': 'error',
        'message': f"Error connecting to the database: {str(e)}",
    })
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