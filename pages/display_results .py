import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from resume_checker.data_fetcher import get_technologies_from_database
from Logs.logging_setup import initialize_logging

st.sidebar.markdown("# Display results ❄️")

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

df = get_technologies_from_database()
search_words = prepare_df(df)

if df is not None and not df.empty:
    st.markdown("<h2 style='text-align: center;'>Enter words to search for:</h2>", unsafe_allow_html=True)
    
    selected_search_words = st.multiselect('', search_words)
    
    st.markdown("<h2 style='text-align: center;'>All job offers:</h2>", unsafe_allow_html=True)

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