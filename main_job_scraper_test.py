import streamlit as st
import subprocess
import os
import time
import logging
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
st.set_page_config(layout="wide")
st.sidebar.markdown("# Job scraper 🎈")
def run_script(script_name):
    try:
        subprocess.run(['python', script_name], check=True, text=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        st.error(f"Error executing script: {e.stderr}")
    else:
        st.success("Script executed successfully!")

def run_job(job_name):
    subprocess.run(["python", os.path.join("app", f"{job_name}.py")])

def run_jobs(args):
    if args['job'] == 'main_job_scraper':
        if args['match']:
            run_job(args['job'])
            time.sleep(5)
            run_job(args['match'])
        else:
            run_job(args['job'])
    elif args['job'] == 'job_scraper_scheduler':
        if args['interval'] is None or args['interval'] >= 90:
            run_job(args['job'])
    else:
        print("Use main_job_scraper or job_scraper_scheduler.")

st.header("Job scraper")
job_name = st.selectbox("Select job to run:", ['main_job_scraper', 'job_scraper_scheduler'])

interval = None  
match_job = None 

if job_name == 'main_job_scraper':
    match_job = st.selectbox("Select matching job for main_job_scraper or None:", ['resume_data_processor', None], key="match_job")
elif job_name == 'job_scraper_scheduler':
    interval = st.number_input("Enter interval for job_scraper_scheduler (in minutes):", min_value=90, value=90)

if st.button("Run Job"):
    args = {
            'job': job_name,
            'interval': interval,
            'match': match_job if job_name == 'main_job_scraper' else None
        }
    with st.status("Downloading data...", expanded=False) as status:
        run_jobs(args)
        status.update(label="Download complete!", state="complete", expanded=False)

