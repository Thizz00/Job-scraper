import pytest
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv('.env')

DATABASE_URL_LOGS = os.getenv('DATABASE_URL_LOGS')

# Create a MongoDB client
client = MongoClient(DATABASE_URL_LOGS, server_api=ServerApi('1'))

def test_mongo_connection():
    try:
        mongo_db = client['Logs']
        log_collection = mongo_db['Logs_scraper']

        assert log_collection.count_documents({}) >= 0

    except Exception as e:
        pytest.fail(f"Error connecting to the database: {e}")

    finally:
        client.close()

def test_env_variable_set():
    assert DATABASE_URL_LOGS is not None
