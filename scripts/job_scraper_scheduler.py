import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main_job_scraper import process_links,scrape_jobs,add_data_to_mysql_db
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from argparse import ArgumentParser
import subprocess

from src.logs_configure.logger_config import configure_logger
import datetime

logger = configure_logger(__name__)

def run_all_modules():
    links = process_links()
    df = scrape_jobs(links)
    add_data_to_mysql_db(df)

def configure_scheduler(interval):
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        run_all_modules,
        trigger=IntervalTrigger(minutes=interval),
        initial_delay=60
    )
    next_run_time = datetime.datetime.now() + datetime.timedelta(minutes=interval)
    logger.info(f"Job will run again at {next_run_time}")
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

    run_all_modules()


    scheduler = configure_scheduler(args.interval)
    scheduler.start()

    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()