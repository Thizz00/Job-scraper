import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.database_initializer import initialize_database
from database.job_offers_db_operations import add_data_to_database
from Logs.logging_setup import initialize_logging
from core.job_scraper import JobScraper
from core.link_processor import LinkProcessor
from core.job_search_url_generator import URLS
from datetime import datetime
import logging

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


def add_data_to_db(df):
    engine, session = initialize_database()
    logging.info("Module 3: Adding data to the database")
    add_data_to_database(session, df)
    session.close()
    logging.info("Database completed.")


if __name__ == '__main__':
    initialize_logging()
    logging.info("Program starts at {}".format(datetime.now()))

    links = process_links()
    df = scrape_jobs(links)
    add_data_to_db(df)

    logging.info("Program execution completed at {}".format(datetime.now()))