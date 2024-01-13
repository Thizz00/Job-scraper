from pydantic import BaseModel

class JobOfferCreate(BaseModel):
    category: list[str] | str 
    link: list[str] | str 
    offer: list[str] | str 
    company_name: list[str] | str 
    salary: list[str] | str 
    tech_stack: list[str] | str 
    type_of_work: list[str] | str 
    experience: list[str] | str 
    employment_type: list[str] | str 
    operating_mode: list[str] | str 
    job_description: list[str] | str 
    application_form: str
    scraping_date: str
