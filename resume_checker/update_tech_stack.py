from resume_checker.data_fetcher import get_technologies_from_database
import pandas as pd


def get_technology_stack():
    df = pd.DataFrame(get_technologies_from_database())
    df = df.apply(lambda col: col.astype(str).str.split(','))
    return df

def update_tech_stack_column(df):
    df['tech_stack'] = df['tech_stack'].apply(lambda row: [tech.upper() for tech in row])
    return df

tech_stack_list = get_technology_stack()
tech_stack_list = update_tech_stack_column(tech_stack_list)

