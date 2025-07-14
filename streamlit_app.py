import streamlit as st

pg = st.navigation([
    st.Page("knowledge_page.py", title="Тест базы знаний", icon=":material/favorite:"),
    st.Page("FAQ_page.py", title="Тест FAQ", icon="🔥"),
])
pg.run()
