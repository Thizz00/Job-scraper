import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from database.init_database import initialize_database

def get_technologies_from_database():
    engine, session = initialize_database()
    query = "SELECT link,tech_stack FROM job_offers"
    df = pd.read_sql(query, engine)

    tech = df
    return tech

