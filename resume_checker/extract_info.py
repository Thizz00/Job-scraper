import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pdfminer.high_level import extract_text
from geotext import GeoText
from tech_data_preparing import tech_stack_list
import pandas as pd
from database.tech_database_operations import initialize_database, add_data_to_database

def extract(url):
    try:
        text = extract_text(url)
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        sys.exit(1)

def plain_text(text):
    return text

def extract_city(text):
    places = GeoText(plain_text(text))
    return(places.cities)

def check_match(tech_tools, result_list):
    tech_tools = set(tech_tools)
    intersection = tech_tools.intersection(result_list) 
    return len(intersection) >= len(tech_tools) / 2

def process_tech_stack_list(url, tech_stack_df):
    extracted_text = extract(url)
    text = plain_text(extracted_text)

    lines = text.splitlines()

    words_list = []

    for line in lines:
        words = line.upper().split()
        words_list.extend(words)

    result_list = set(words_list)

    tech_stack_df['matched'] = tech_stack_df['tech_stack'].apply(lambda x: check_match(x, result_list))

    return tech_stack_df

def convert_list_to_str(df):
    df['tech_stack'] = df['tech_stack'].apply(str)
    return df

def add_data_to_db(df):
    engine, session = initialize_database()
    add_data_to_database(session, df)
    session.close()

    
if __name__ == "__main__":
    url = 'test.pdf'
    df = process_tech_stack_list(url, tech_stack_list)
    df = convert_list_to_str(df)
    add_data_to_db(df)