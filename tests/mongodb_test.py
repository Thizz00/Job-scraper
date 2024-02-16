import pytest

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv

from pymongo import MongoClient
from pymongo.server_api import ServerApi

load_dotenv('.env')

DATABASE_URL_LOGS = os.getenv('DATABASE_URL_LOGS')


def test_env_variable_set():
    assert DATABASE_URL_LOGS is not None


def test_mongo_connection():

    client = MongoClient(DATABASE_URL_LOGS, server_api=ServerApi('1'))

    mongo_db = client['Logs']
    log_collection = mongo_db['Logs_scraper']

    assert 'Logs_scraper' in mongo_db.list_collection_names()

    assert log_collection.count_documents({}) >= 0

    client.close()
