from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv('.env')

DATABASE_URL_LOGS = os.getenv('DATABASE_URL_LOGS')

client = MongoClient(DATABASE_URL_LOGS, server_api=ServerApi('1'))

mongo_db = client['Logs']
log_collection = mongo_db['Logs_scraper']