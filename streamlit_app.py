import streamlit as st
import langchain_community
import pandas as pd
#import faiss
from langchain_community.vectorstores.faiss import FAISS
from openai import OpenAI
from langchain.document_loaders import DataFrameLoader

# Show title and description.
st.title("📄 Задавайте вопросы по тексту")
#st.write(
#    "Upload a document below and ask a question about it – GPT will answer! "
openai_api_key = st.secrets["OPENAI_API_KEY"]
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    model = st.selectbox(
      "Выберите ИИ модель:",
      ("gpt-4.1", "o4-mini", "gpt-4o"),
    )
    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Загрузите свой текст здесь (.txt или .md)", type=("txt", "md")
    )
    # 
    input_text = st.text_area(
        "Либо скопируйте свой текст прямо сюда:",
        placeholder=" ",
    #    disabled= uploaded_file,
    )
    
    st.divider()

    with st.form("qa_form"):
       st.write("Заведите свои ЧаВо")
       df = pd.DataFrame(
           [
              {"Вопрос": "?", "Ответ": "2"},
              {"Вопрос": "?", "Ответ": "4"},
              {"Вопрос": "?", "Ответ": "3"},
          ]
       )
       edited_df = st.data_editor(df)
       qa_submitted = st.form_submit_button("Отправить") 
       loader = DataFrameLoader(
           dataframe = df,
           page_content_column = "Вопрос"
        )
       documents = loader.load()
    st.write(Documents)
    st.divider()

    with st.form("question_form"):
        question = st.text_input("Задайте вопрос по тексту:", "")
        q_submitted = st.form_submit_button("Отправить")
    if q_submitted:
        if uploaded_file: 
           # Process the uploaded file and question.
           document = uploaded_file.read().decode()
           messages = [
               {
                   "role": "user",
                   "content": f"Here's a document: {document} \n\n---\n\n {question}",
               }
             ]
        elif input_text:
           # Process input text and question.
           document = input_text
           messages = [
                {
                    "role": "user",
                    "content": f"Here's a document: {document} \n\n---\n\n {question}",
                }
              ]
        # Generate an answer using the OpenAI API.
        stream = client.chat.completions.create(
              model=model,
              messages=messages,
              stream=True,
          )

        # Stream the response to the app using `st.write_stream`.
        st.write_stream(stream)
