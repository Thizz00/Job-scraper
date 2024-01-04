import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.init_database import initialize_database
from core.job_search_url_generator import generate_all_urls
from database.database_operations import add_data_to_database
from core.job_scraper import JobScraper
from core.link_processor import LinkProcessor
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from datetime import datetime
from argparse import ArgumentParser
import subprocess



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


def initialize():
    global URLS, df, links
    URLS = generate_all_urls()
    df, links = None, None


def run_module(module_func, module_name):
    try:
        logging.info(f"{module_name}: Started")
        result = module_func()
        logging.info(f"{module_name}: {'Completed'}")
        return result
    except Exception as e:
        logging.error(f"Error in {module_name}: {e}")
        return False


def process_links():
    logging.info("Module 1: Link Processing")
    global links
    link_processor = LinkProcessor(URLS)
    link_processor.process_urls()
    links = link_processor.scraped_links
    logging.info("Link processing completed.")


def scrape_jobs():
    logging.info("Module 2: Job Scraping")
    global df, links
    job_scraper = JobScraper(links)
    job_scraper.scrape_jobs()
    df = job_scraper.df
    logging.info("Job scraping completed.")


def add_data_to_db():
    logging.info("Module 3: Adding data to the database")
    engine, session = initialize_database()
    add_data_to_database(session, df)
    session.close()
    logging.info("Database completed.")


def run_all_modules():
    modules = [process_links, scrape_jobs, add_data_to_db]
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
    script_path = os.path.join("app", f"{job_name}.py")
    subprocess.run(["python",
                    script_path,
                    "--interval",
                    str(interval)])


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--interval', type=int, default=90)

    args = parser.parse_args()

    setup_logging()
    logging.info("Program starts at {}".format(datetime.now()))
    initialize()
    run_all_modules()
    logging.info("Program execution completed at {}".format(datetime.now()))

    scheduler = configure_scheduler(args.interval)
    scheduler.start()

    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()