import streamlit as st
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from resume_checker.data_fetcher import get_technologies_from_database
from Logs.logging_setup import initialize_logging
from database.database_initializer import initialize_database
import pandas as pd

st.sidebar.markdown("# Display match results ❄️")
initialize_logging()

def get_technologies_from_database():
    engine, session = initialize_database()
    query = "SELECT * FROM tech_tools order by matched DESC"
    df = pd.read_sql(query, engine)
    return df

df = get_technologies_from_database()

if df is not None and not df.empty:
    st.markdown("<h2 style='text-align: center;'>All job offers:</h2>", unsafe_allow_html=True)

    st.data_editor(
        df,
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
