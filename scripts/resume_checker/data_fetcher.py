import pandas as pd
from src.database.database_initializer import initialize_database

engine, session = initialize_database()

def get_technologies_from_database():
    query = "SELECT * FROM tech_tools"
    df = pd.read_sql(query, engine)

    return df



def get_all_from_database():
    query = "SELECT * FROM job_offers"
    df = pd.read_sql(query, engine)

    return df
