import argparse
import logging
from resume_checker.tech_data_preparing import tech_stack_list
from resume_checker.extract_info import process_tech_stack_list, convert_list_to_str, add_data_to_db

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--match')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    if args.match:
        try:
            df = process_tech_stack_list(args.match, tech_stack_list)
            df = convert_list_to_str(df)
            add_data_to_db(df)
            logging.info(f'Successfully processed and added data to the database.')
        except Exception as e:
            logging.error(f'Error processing and adding data to the database: {str(e)}')
    else:
        logging.warning("Please provide the correct argument")
