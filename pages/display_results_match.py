from scripts.resume_checker.data_fetcher import get_technologies_from_database
import streamlit as st

st.sidebar.markdown("# Display match results ⚙️")


df = get_technologies_from_database()

if df is not None and not df.empty:
    st.markdown("<h2 style='text-align: center;'>All job offers:</h2>", unsafe_allow_html=True)

    st.data_editor(
        df,
        column_config={
            "link": st.column_config.LinkColumn(),
        },
        disabled = ["id","link","tech_stack","matched"],
        hide_index=True,
    )

else:
    col1, col2, col3 = st.columns(3)
    col1.write("")
    with col2:
        st.markdown("<h2 style='text-align: center;'>No job offers.</h2>", unsafe_allow_html=True)
    col3.write("")