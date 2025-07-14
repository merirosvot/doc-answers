import streamlit as st

pg = st.navigation([
    st.Page("knowledge_page.py", title="First page", icon=":material/favorite:"),
    st.Page("FAQ_page.py", title="Second page", icon="🔥"),
], position="top")
pg.run()
