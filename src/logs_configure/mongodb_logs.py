from src.models.job_offer import JobOffer
from src.models.tech_tools import TechTools

def create_log_entryTechTools(job_offer):
    entry = {'level': 'Success'}
    for column in TechTools.__table__.columns:
        entry[column.name] = str(getattr(job_offer, column.name))
    return entry

def create_log_entryJobOffers(job_offer):
    entry = {'level': 'Success'}
    for column in JobOffer.__table__.columns:
        entry[column.name] = str(getattr(job_offer, column.name))
    return entry
