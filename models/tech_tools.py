from config.base import Base
from sqlalchemy import Column, Integer, Text

class TechTools(Base):
    __tablename__ = 'tech_tools'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tech_stack = Column(Text)
    category = Column(Text(4))
    