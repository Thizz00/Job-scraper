import streamlit as st
import subprocess

from Logs.logging_setup import initialize_logging
from app.main_job_scraper import process_links,scrape_jobs,add_data_to_db1
from app.resume_data_processor import process_tech_stack_list, convert_list_to_str, add_data_to_db, tech_stack_list, find_newest_file
from datetime import datetime
import logging

st.set_page_config(layout="wide")
st.sidebar.markdown("# Job scraper 🎈")
initialize_logging()

with st.columns(3)[1]:
    st.header("Job scraper")
    job_name = st.selectbox("Select job to run:", ['main_job_scraper', 'job_scraper_scheduler','resume_data_processor'])

    interval = None  
    match_job = None 

    if job_name == 'main_job_scraper':
        match_job = st.selectbox("Select matching job for main_job_scraper or None:", ['resume_data_processor', None], key="match_job")
    elif job_name == 'job_scraper_scheduler':
        interval = st.number_input("Enter interval for job_scraper_scheduler (in minutes):", min_value=90, value=90)
    run_button = st.button("Run Job")

    if run_button:
        if job_name == 'main_job_scraper' and match_job is None:
            with st.status("Job enabled.", expanded=True) as status:
                try:
                    initialize_logging()
                    logging.info("Program starts at {}".format(datetime.now()))
                    st.write("Process links ⏳")
                    links = process_links()
                    st.write("Process links ✔️")
                            
                    st.write("Scraping jobs ⏳")
                    df = scrape_jobs(links)
                    st.write("Scraping jobs ✔️")
                            
                    st.write("Add data to databases ⏳")
                    add_data_to_db1(df)
                    st.write("Add data to databases ✔️")
                            
                    logging.info("Program execution completed at {}".format(datetime.now()))
                except Exception as e:
                    st.error(f"Error: {str(e)}")

                status.update(label="Job successfully completed!", state="complete", expanded=False)


        elif job_name == 'main_job_scraper' and match_job == 'resume_data_processor':
            with st.status("Job enabled.", expanded=True) as status:
                try:
                    initialize_logging()
                    logging.info("Program starts at {}".format(datetime.now()))
                    st.write("Process links ⏳")
                    links = process_links()
                    st.write("Process links ✔️")
                                
                    st.write("Scraping jobs ⏳")
                    df = scrape_jobs(links)
                    st.write("Scraping jobs ✔️")
                                
                    st.write("Add data to databases ⏳")
                    add_data_to_db(df)
                    st.write("Add data to databases ✔️")
                                

                    PATH = find_newest_file('CV') 
                    st.write("Process resume data ⏳")
                    try:
                        df = process_tech_stack_list(PATH, tech_stack_list)
                        df_str = convert_list_to_str(df)
                        add_data_to_db(df_str)
                        st.write("Process resume data completed ✔️")
                        logging.info('Successfully processed and added data to the database.')
                    except Exception as e:
                        logging.error(f'Error processing and adding data to the database: {str(e)}')

                    logging.info("Program execution completed at {}".format(datetime.now()))
                except Exception as e:
                    st.error(f"❌: {str(e)}")

                status.update(label="Job successfully completed!", state="complete", expanded=False)


        elif job_name == 'job_scraper_scheduler':
            with st.status("Job enabled.", expanded=True) as status:
                subprocess.run(["python", "app/job_scraper_scheduler.py", "--interval", str(interval)])
                status.update(label="Job successfully completed!", state="complete", expanded=False)


        elif job_name == 'resume_data_processor':
            with st.status("Job enabled.", expanded=True) as status:
                subprocess.run(["python", "app/resume_data_processor.py"])
                status.update(label="Job successfully completed!", state="complete", expanded=False)