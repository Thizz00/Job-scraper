import streamlit as st
import subprocess

st.set_page_config(layout="wide")
st.sidebar.markdown("# Job scraper 🎈")

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
    try:
        if job_name == 'main_job_scraper' and match_job  ==  None:
            subprocess.run(["python", "app/main_job_scraper.py"])

        elif job_name == 'main_job_scraper' and match_job == 'resume_data_processor':
            subprocess.run(["python", "app/main_job_scraper.py", "--match resume_data_processor"])

        elif job_name == 'job_scraper_scheduler':
            subprocess.run(["python", "app/job_scraper_scheduler.py", "--interval", str(interval)])

        elif job_name == 'resume_data_processor':
            subprocess.run(["python", "app/resume_data_processor.py"])
    except Exception as e:
        st.write(f"Error {str(e)}")
