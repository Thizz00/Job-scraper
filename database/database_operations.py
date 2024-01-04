import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pydantic import ValidationError
from database.init_database import handle_database_error
from config.db_logs import log_collection
from models.joboffer import JobOffer
from schemas.job_offer import JobOfferCreate
import logging


def add_data_to_database(session, df):
    try:
        for _, row in df.iterrows():
            try:
                job_offer_data = JobOfferCreate(**row)
            except ValidationError as e:
                for error in e.errors():
                    logging.error(f"Validation error: {error['loc']} - {error['msg']}")
                continue

            new_job_offer = create_job_offer_instance(job_offer_data)
            existing_offer = session.query(JobOffer).filter_by(link=new_job_offer.link).first()
            
            if existing_offer:
                update_existing_offer(session, existing_offer, new_job_offer)
            else:
                session.add(new_job_offer)
                logging.info(f"Inserted new job offer into the database: {new_job_offer.link}")
                log_entry = create_log_entry(new_job_offer)
                log_collection.insert_one(log_entry)

        session.commit()
    except Exception as e:
        handle_database_error(e)
        session.rollback()
    finally:
        session.close()

def create_job_offer_instance(job_offer_data):
    return JobOffer(
        category=job_offer_data.category,
        link=job_offer_data.link,
        offer=job_offer_data.offer,
        company_name=job_offer_data.company_name,
        salary=job_offer_data.salary,
        tech_stack=job_offer_data.tech_stack,
        type_of_work=job_offer_data.type_of_work,
        experience=job_offer_data.experience,
        employment_type=job_offer_data.employment_type,
        operating_mode=job_offer_data.operating_mode,
        job_description=job_offer_data.job_description,
        application_form=job_offer_data.application_form,
        scraping_date=job_offer_data.scraping_date
    )

def update_existing_offer(session, existing_offer, new_job_offer):
    columns_to_update = [
        'category', 'offer', 'company_name', 'salary',
        'tech_stack', 'type_of_work', 'experience',
        'employment_type', 'operating_mode', 'job_description',
        'application_form', 'scraping_date'
    ]

    differences_found = False 

    for column in columns_to_update:
        existing_value = getattr(existing_offer, column)
        new_value = getattr(new_job_offer, column)

        if existing_value != new_value:
            differences_found = True
            setattr(existing_offer, column, new_value)

    if differences_found:
        logging.info(f"Updated existing job offer in the database: {existing_offer.link}")
        log_entry = create_log_entry(existing_offer)
        log_collection.insert_one(log_entry)

def create_log_entry(job_offer):
    entry = {'level': 'Success'}
    for column in JobOffer.__table__.columns:
        entry[column.name] = str(getattr(job_offer, column.name))
    return entry

