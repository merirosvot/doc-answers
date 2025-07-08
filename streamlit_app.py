import streamlit as st
import os
from openai import OpenAI

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
    
    # Ask the user for a question via `st.text_area`.
    question = st.text_area(
        "Задайте вопрос по тексту:",
        placeholder="Расскажи, о чем этот текст?",
#        disabled=not uploaded_file,
    )

    if question:
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
