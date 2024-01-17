import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from src.database.database_initializer import initialize_database
from src.database.job_offers_db_operations import add_data_to_db_all
from scripts.core.job_scraper import JobScraper
from scripts.core.link_processor import LinkProcessor
from scripts.core.job_search_url_generator import URLS
import logging
from src.logs_configure.logging_setup import initialize_logging
from datetime import datetime

def process_links():
    logging.info("Module 1: Link Processing")
    link_processor = LinkProcessor(URLS)
    link_processor.process_urls()
    links = link_processor.scraped_links
    logging.info("Link processing completed.")
    return links


def scrape_jobs(links):
    logging.info("Module 2: Job Scraping")
    job_scraper = JobScraper(links)
    job_scraper.scrape_jobs()
    df = job_scraper.df
    logging.info("Job scraping completed.")
    return df


def add_data_to_mysql_db(df):
    engine, session = initialize_database()
    logging.info("Module 3: Adding data to the database")
    add_data_to_db_all(session, df)
    session.close()
    logging.info("Database completed.")


if __name__ == '__main__':
    initialize_logging()
    logging.info("Program starts at {}".format(datetime.now()))

    links = process_links()
    df = scrape_jobs(links)
    add_data_to_mysql_db(df)

    logging.info("Program execution completed at {}".format(datetime.now()))