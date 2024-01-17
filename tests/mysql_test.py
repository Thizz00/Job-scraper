import pytest
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

from src.config.db_data import Base
from sqlalchemy.orm import sessionmaker

load_dotenv('.env')

DATABASE_URL = os.getenv('DATABASE_URL')

def test_mysql_connection():
    try:
        engine = create_engine(DATABASE_URL, echo=True)

        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)

        with Session() as session:
            result = session.execute("SELECT 1")
            assert result.scalar() == 1, "Unexpected result from the query"

    except Exception as e:
        pytest.fail(f"Error connecting to the database: {e}")

    finally:
        session.close()

def test_env_variable_set():
    assert DATABASE_URL is not None