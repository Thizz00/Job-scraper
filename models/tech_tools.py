from config.base import Base
from sqlalchemy import Column, Integer, Text, Boolean

class TechTools(Base):
    __tablename__ = 'tech_tools'
    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(Text)
    tech_stack = Column(Text)
    matched = Column(Boolean)
