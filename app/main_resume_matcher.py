import os
import sys
from pathlib import Path


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging

from resume_checker.tech_data_preparing import tech_stack_list
from resume_checker.extract_info import process_tech_stack_list, convert_list_to_str, add_data_to_db

def setup_logging():
    log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file = os.path.join(log_dir, 'Logs/logs.txt')
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
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
    setup_logging()
    PATH = find_newest_file('CV') 

    try:
        df = process_tech_stack_list(PATH,tech_stack_list)
        df = convert_list_to_str(df)
        add_data_to_db(df)
        logging.info(f'Successfully processed and added data to the database.')
    except Exception as e:
        logging.error(f'Error processing and adding data to the database: {str(e)}')
else:
    logging.warning("Please provide the correct argument")
