import streamlit as st
import pandas as pd
import langchain 
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.document_loaders import DataFrameLoader
from langchain_core.vectorstores import InMemoryVectorStore

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
#    embeddings_ai = client.embeddings.create(input = "Test", model="text-embedding-3-small")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
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
# Форма для ввода вопроса пользователя
    with st.form("question_form"):
        question = st.text_input("Задайте вопрос по тексту:", "")
        q_submitted = st.form_submit_button("Отправить")
    if q_submitted:
        if uploaded_file: 
           # Process the uploaded file and question.
           document = uploaded_file.read().decode()
        elif input_text:
           # Process input text and question.
           document = input_text
        messages = [
            {"role": "system", "content": f"Отвечай используя информацию из документа"},
            {"role": "user", "content": f"Документ: {document} \n\n---\n\n {question}",}
        ]
        # Generate an answer using the OpenAI API.
        stream = client.chat.completions.create(
              model=model,
              messages=messages,
              stream=True,
          )
        # Stream the response to the app using `st.write_stream`.
        st.write_stream(stream)
    st.divider()

# Форма для ввода пар вопросов и ответов
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
           data_frame = edited_df,
           page_content_column = "Вопрос"
        )
    if qa_submitted:
       documents = loader.load()
       st.write(documents)
       text_splitter = RecursiveCharacterTextSplitter(
       chunk_size=1000, chunk_overlap=200, add_start_index=True
       )
       all_splits = text_splitter.split_documents(documents)
       len(all_splits)
       vector_store = InMemoryVectorStore(embeddings)
       ids = vector_store.add_documents(documents=all_splits)
       results = vector_store.similarity_search("www?")
       print(results[0])
