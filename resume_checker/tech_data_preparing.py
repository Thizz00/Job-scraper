from test import get_technologies_from_database
import pandas as pd
import logging
from database.tech_database_operations import initialize_database, add_data_to_database

def get_technology_stack():
    df = pd.DataFrame(get_technologies_from_database())
    return df['Tech_stack'].str.split(',').explode().str.upper().tolist()

def clean_encoding(key):
    try:
        return key.encode('cp1252', 'ignore').decode('cp1252')
    except UnicodeEncodeError as e:
        logging.error(f"Ignoring element due to encoding error: {key}, Error: {e}")
        return None

def clean_tech_dictionary(tech_dict):
    return {clean_encoding(key): value for key, value in tech_dict.items()}

def display_tech(tech_dict):
    df = pd.DataFrame(list(tech_dict.items()), columns=['Tech', 'Category'])
    return df

def add_data_to_db(df):
    logging.info("Module 3: Adding data to the database")
    engine, session = initialize_database()
    add_data_to_database(session, df)
    session.close()
    logging.info("Database completed.")

def main():
    tech_stack_list = get_technology_stack()
    tech_dict = {element: "Tech" for element in set(tech_stack_list)}
    cleaned_tech_dict = clean_tech_dictionary(tech_dict)
    unique_tech_dict = dict.fromkeys(cleaned_tech_dict, "Tech")
    df = display_tech(unique_tech_dict)
    add_data_to_db(df)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
