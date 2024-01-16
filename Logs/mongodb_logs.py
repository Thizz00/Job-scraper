from models.tech_tools import TechTools
from models.job_offer import JobOffer
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
