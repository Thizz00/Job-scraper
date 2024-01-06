import streamlit as st
import subprocess
import os
import time
import streamlit as st
import logging
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from resume_checker.data_fetcher import get_technologies_from_database
from Logs.logging_setup import initialize_logging

st.set_page_config(layout="wide")
initialize_logging()

def prepare_df(df):
    category_words = set(word.strip().upper() for word in df['category'] if word is not None)
    tech_stack_words = set(word.strip().upper() for word in df['tech_stack'] if word is not None)

    search_words = list(category_words.union(tech_stack_words))
    search_words = [word for line in search_words for word in line.replace(', ', ',').split(',')]

    search_words = list(set(search_words))

    return search_words

def contains_all_search_words(row, selected_search_words):
    category_words = [word.strip().upper() for word in (row['category'].split(', ') if row['category'] else [])]
    tech_stack_words = [word.strip().upper() for word in (row['tech_stack'].split(', ') if row['tech_stack'] else [])]

    return all(word in category_words or word in tech_stack_words for word in selected_search_words)

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

df = get_technologies_from_database()
if df is not None and not df.empty:
    search_words = prepare_df(df)
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
        with st.status("Downloading data...", expanded=True) as status:
            run_jobs(args)
            status.update(label="Download complete!", state="complete", expanded=False)


    if st.button('Display results'):
        col1, col2, col3 = st.columns(3)
        col1.write("")

        with col2:
            st.markdown("<h2 style='text-align: center;'>Enter words to search for:</h2>", unsafe_allow_html=True)
            selected_search_words = st.multiselect('', search_words)

        col3.write("")

        col1, col2, col3 = st.columns(3)
        col1.write("")

        with col2:
            st.markdown("<h2 style='text-align: center;'>All job offers:</h2>", unsafe_allow_html=True)

        col3.write("")

        filtered_df = df[df.apply(contains_all_search_words, axis=1, selected_search_words=selected_search_words)]
        st.data_editor(
            filtered_df,
            column_config={
                "link": st.column_config.LinkColumn(),
            },
            hide_index=True,
        )

else:
    col1, col2, col3 = st.columns(3)
    col1.write("")

    with col2:
        st.markdown("<h2 style='text-align: center;'>No job offers. </h2>", unsafe_allow_html=True)

    col3.write("")
