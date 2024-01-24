import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.database_initializer import initialize_database
from core.job_search_url_generator import generate_all_urls
from src.database.job_offers_db_operations import add_data_to_db_all
from core.job_scraper import JobScraper
from core.link_processor import LinkProcessor
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from argparse import ArgumentParser
import subprocess

from src.logs_configure.logger_config import configure_logger

logger = configure_logger(__name__)


def initialize():
    global URLS, df, links
    URLS = generate_all_urls()
    df, links = None, None


def run_module(module_func, module_name):
    logger.info(f"{module_name}: Started")
    result = module_func()
    logger.info(f"{module_name}: {'Completed'}")
    return result


def process_links():
    logger.info("Module 1: Link Processing")
    global links
    link_processor = LinkProcessor(URLS)
    link_processor.process_urls()
    links = link_processor.scraped_links
    logger.info("Link processing completed.")


def scrape_jobs():
    logger.info("Module 2: Job Scraping")
    global df, links
    job_scraper = JobScraper(links)
    job_scraper.scrape_jobs()
    df = job_scraper.df
    logger.info("Job scraping completed.")


def add_data_to_mysql_db():
    logger.info("Module 3: Adding data to the database")
    engine, session = initialize_database()
    add_data_to_db_all(session, df)
    session.close()
    logger.info("Database completed.")


def run_all_modules():
    modules = [process_links, scrape_jobs, add_data_to_mysql_db]
    for module_func in modules:
        module_name = module_func.__name__.title()
        run_module(module_func, module_name)


def configure_scheduler(interval):
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        run_all_modules,
        trigger=IntervalTrigger(minutes=interval),
        initial_delay=60
    )
    return scheduler


def run_job(job_name, interval):
    script_path = os.path.join("scripts/app", f"{job_name}.py")
    subprocess.run(["python",
                    script_path,
                    "--interval",
                    str(interval)])


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--interval', type=int, default=90)

    args = parser.parse_args()
    logger.info("Program starts at {}".format(datetime.now()))
    initialize()
    run_all_modules()
    logger.info("Program execution completed at {}".format(datetime.now()))

    scheduler = configure_scheduler(args.interval)
    scheduler.start()

    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()