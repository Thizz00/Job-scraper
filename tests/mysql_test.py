import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv

from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
from src.config.db_data import Base

load_dotenv('.env')

DATABASE_URL = os.getenv('DATABASE_URL')

def test_env_variable_set():
    assert DATABASE_URL is not None

def test_mysql_connection():
    engine = create_engine(DATABASE_URL, echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    with Session() as session:
        sql = text('select 5')
        result = session.execute(sql)
        assert result.scalar() == 5, "Unexpected result from the query"
