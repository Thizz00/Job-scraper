import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from database.database_initializer import initialize_database

def get_technologies_from_database():
    engine, session = initialize_database()
    query = "SELECT * FROM tech_tools"
    df = pd.read_sql(query, engine)

    return df


def get_all_from_database():
    engine, session = initialize_database()
    query = "SELECT * FROM job_offers"
    df = pd.read_sql(query, engine)

    return df
