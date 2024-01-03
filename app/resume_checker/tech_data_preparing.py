from resume_checker.select_table import get_technologies_from_database
import pandas as pd


def get_technology_stack():
    df = pd.DataFrame(get_technologies_from_database())
    df = df.apply(lambda col: col.astype(str).str.split(','))
    return df

def engineer(df):
    df['tech_stack'] = df['tech_stack'].apply(lambda row: [tech.upper() for tech in row])
    return df

tech_stack_list = get_technology_stack()
tech_stack_list = engineer(tech_stack_list)

