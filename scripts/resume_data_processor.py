import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from pathlib import Path
from resume_checker.update_tech_stack import tech_stack_list
from resume_checker.text_extraction_utils import convert_list_to_str,add_data_tech_to_db,process_tech_stack_list
from src.logs_configure.logger_config import configure_logger
import datetime

logger = configure_logger(__name__)

def find_newest_file(folder_path):
    folder = Path(folder_path)

    if not folder.is_dir():
        logger.error(f"Folder '{folder_path}' does not exist.")
        return None

    pdf_files = [file for file in folder.iterdir() if file.is_file() and file.suffix.lower() == '.pdf']

    if not pdf_files:
        logger.warning(f"No PDF files in the folder '{folder_path}'.")
        return None

    newest_file = max(pdf_files, key=lambda x: x.stat().st_mtime)

    logger.info(f"Newest PDF file found: {newest_file}")

    return newest_file

if __name__ == "__main__":

    logger.info("Program starts at {}".format(datetime.now()))
    PATH = find_newest_file('CV') 
    df = process_tech_stack_list(PATH, tech_stack_list)
    df_str = convert_list_to_str(df)
    add_data_tech_to_db(df_str)
    logger.info("Program execution completed at {}".format(datetime.now()))
