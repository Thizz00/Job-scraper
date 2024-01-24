import streamlit as st
import subprocess
from scripts.main_job_scraper import process_links, add_data_to_mysql_db, scrape_jobs
from datetime import datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.logs_configure.logger_config import configure_logger

logger = configure_logger(__name__)

st.set_page_config(layout="wide")
st.sidebar.markdown("# Job scraper 📊")


def run_main_job_scraper():
    with st.status("Job enabled.", expanded=True) as status:
        try:
            logger.info("Program starts at {}".format(datetime.now()))
            st.write("Process links ⏳")
            links = process_links()
            st.write("Process links ✔️")

            st.write("Scraping jobs ⏳")
            df = scrape_jobs(links)
            st.write("Scraping jobs ✔️")

            st.write("Add data to databases ⏳")
            add_data_to_mysql_db(df)
            st.write("Add data to databases ✔️")

            logger.info("Program execution completed at {}".format(datetime.now()))
        except Exception as e:
            logger.error(f"Exception occurred: {str(e)}")
            st.error(f"Exception occurred: {str(e)}")

        status.update(label="Job successfully completed!", state="complete", expanded=False)

def run_resume_data_processor():
    with st.status("Job enabled.", expanded=False) as status:
        try:
            logger.info("Program starts at {}".format(datetime.now()))

            subprocess.run(["python", "scripts/resume_data_processor.py"])

            status.update(label="Job successfully completed!", state="complete", expanded=False)
            logger.info("Program execution completed at {}".format(datetime.now()))
        except Exception as e:
            st.error(f"❌: {str(e)}")

        status.update(label="Job successfully completed!", state="complete", expanded=False)

def run_job_scraper_scheduler(interval):
    with st.status("Job enabled.", expanded=False) as status:
        subprocess.run(["python", "scripts/job_scraper_scheduler.py", "--interval", str(interval)])
        status.update(label="Job successfully completed!", state="complete", expanded=False)

with st.columns(3)[1]:
    st.header("Job scraper")
    job_name = st.selectbox("Select job to run:", ['main_job_scraper', 'job_scraper_scheduler','resume_data_processor'])
    interval = None  

    if job_name == 'main_job_scraper':
        run_button = st.button("Run Job")
        if run_button:
            run_main_job_scraper()

            
    elif job_name == 'resume_data_processor':
        run_button = st.button("Run Job")
        if run_button:
            run_resume_data_processor()


    elif job_name == 'job_scraper_scheduler':
        interval = st.number_input("Enter interval for job_scraper_scheduler (in minutes):", min_value=90, value=90)
        run_button = st.button("Run Job")
        if run_button:
            run_job_scraper_scheduler(interval)

