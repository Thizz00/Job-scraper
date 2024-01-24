import streamlit as st
from scripts.resume_checker.data_fetcher import get_all_from_database
from nltk.stem import PorterStemmer

st.sidebar.markdown("# Display results 🎯")



def prepare_df(df):
    search_words = set()
    for column in ['category', 'tech_stack']:
        words = df[column].dropna().str.upper().str.replace(', ', ',').str.split(',')
        search_words.update(word for sublist in words for word in sublist)

    return list(search_words)


def contains_all_search_words(row, selected_search_words):
    category_words = set(word.strip().upper() for word in (row['category'].split(', ') if row['category'] else []))
    tech_stack_words = set(word.strip().upper() for word in (row['tech_stack'].split(', ') if row['tech_stack'] else []))

    all_words = category_words.union(tech_stack_words)

    return all(word in all_words for word in selected_search_words)




df = get_all_from_database()
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
        disabled = ["id","category","link","offer","company_name","salary","tech_stack","type_of_work","experience","employment_type","operating_mode","job_description","application_form","scraping_date"],
        hide_index=True,
    )

else:
    col1, col2, col3 = st.columns(3)
    col1.write("")

    with col2:
        st.markdown("<h2 style='text-align: center;'>No job offers. </h2>", unsafe_allow_html=True)

    col3.write("")