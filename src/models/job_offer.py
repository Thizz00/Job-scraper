from src.config.db_data import Base
from sqlalchemy import Column, Integer, Text

class JobOffer(Base):
    __tablename__ = 'job_offers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(Text)
    link = Column(Text(256), unique=True)
    offer = Column(Text)
    company_name = Column(Text)
    salary = Column(Text)
    tech_stack = Column(Text)
    type_of_work = Column(Text)
    experience = Column(Text)
    employment_type = Column(Text)
    operating_mode = Column(Text)
    job_description = Column(Text)
    application_form = Column(Text)
    scraping_date = Column(Text) 

    