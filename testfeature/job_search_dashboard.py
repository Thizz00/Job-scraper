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

def contains_all_search_words(row):
    category_words = [word.strip().upper() for word in (row['category'].split(', ') if row['category'] else [])]
    tech_stack_words = [word.strip().upper() for word in (row['tech_stack'].split(', ') if row['tech_stack'] else [])]

    return all(word in category_words or word in tech_stack_words for word in selected_search_words)

try:
    df = get_technologies_from_database()
    if df:
        search_words = prepare_df(df)

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

        filtered_df = df[df.apply(contains_all_search_words, axis=1)]
        st.data_editor(
            filtered_df,
            column_config={
                "link": st.column_config.LinkColumn(),
            },
            hide_index=True,
        )
        if st.session_state.display_results:
            st.write("Results are displayed!")
    else:   
        col1, col2, col3 = st.columns(3)
        col1.write("")

        with col2:
            st.markdown("<h2 style='text-align: center;'>No job offers. </h2>", unsafe_allow_html=True)

        col3.write("")



except Exception as e:
    logging.error(f"An error occurred: {e}")
    st.error(f"An error occurred: {e}")