
from pdfminer.high_level import extract_text
from src.database.database_initializer import initialize_database
from src.database.tech_tools_db_operations import add_data_to_database


def extract(url):
    text = extract_text(url)
    return text

def check_match(tech_tools, result_list):
    tech_tools = set(tech_tools)
    intersection = tech_tools.intersection(result_list)
    return len(intersection) >= len(tech_tools) / 2


def process_tech_stack_list(url, tech_stack_df):
    text = extract(url)
    lines = text.splitlines()
    words_list = []

    for line in lines:
        words = line.upper().split()
        words_list.extend(words)

    result_list = set(words_list)
    tech_stack_df['matched'] = tech_stack_df['tech_stack'].apply(lambda x: check_match(x, result_list))

    return tech_stack_df


def convert_list_to_str(df):
    df['tech_stack'] = df['tech_stack'].apply(lambda x: ', '.join(x).capitalize())
    return df


def add_data_tech_to_db(df):
    engine, session = initialize_database()
    add_data_to_database(session, df)
    session.close()
