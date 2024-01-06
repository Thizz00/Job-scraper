import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pathlib import Path
import logging
from resume_checker.update_tech_stack import tech_stack_list
from resume_checker.text_extraction_utils import (
    process_tech_stack_list,
    convert_list_to_str,
    add_data_to_db
)
from Logs.logging_setup import initialize_logging

def find_newest_file(folder_path):
    folder = Path(folder_path)

    if not folder.is_dir():
        logging.error(f"Folder '{folder_path}' does not exist.")
        return None

    pdf_files = [file for file in folder.iterdir() if file.is_file() and file.suffix.lower() == '.pdf']

    if not pdf_files:
        logging.warning(f"No PDF files in the folder '{folder_path}'.")
        return None

    newest_file = max(pdf_files, key=lambda x: x.stat().st_mtime)

    logging.info(f"Newest PDF file found: {newest_file}")

    return newest_file

if __name__ == "__main__":
    initialize_logging()
    PATH = find_newest_file('CV') 

    try:
        df = process_tech_stack_list(PATH, tech_stack_list)
        df_str = convert_list_to_str(df)
        add_data_to_db(df_str)
        logging.info('Successfully processed and added data to the database.')
    except Exception as e:
        logging.error(f'Error processing and adding data to the database: {str(e)}')
else:
    logging.warning("Please provide the correct argument")
