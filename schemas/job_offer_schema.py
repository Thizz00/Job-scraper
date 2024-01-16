from pydantic import BaseModel
from datetime import datetime

class JobOfferCreate(BaseModel):
    category: str
    link: str 
    offer: str 
    company_name: str 
    salary: str 
    tech_stack: str 
    type_of_work: str 
    experience: str 
    employment_type: str 
    operating_mode: str 
    job_description: str 
    application_form: str
    scraping_date: datetime