import streamlit as st
import os
from openai import OpenAI

# Show title and description.
st.title("📄 Задавайте вопросы по тексту")
#st.write(
#    "Upload a document below and ask a question about it – GPT will answer! "
#    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
#)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
# openai_api_key = os.environ["openai_api_key"]
openai_api_key = st.secrets["OPENAI_API_KEY"]
# openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

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

    if uploaded_file and question:

        # Process the uploaded file and question.
        document = uploaded_file.read().decode()
        messages = [
            {
                "role": "user",
                "content": f"Here's a document: {document} \n\n---\n\n {question}",
            }
          ]
        # Generate an answer using the OpenAI API.
        stream = client.chat.completions.create(
              model="gpt-4.1",
              messages=messages,
              stream=True,
           )
        st.write_stream(stream)

    elif input_text and question:

        # Process the uploaded file and question.
        document = input_text
        messages = [
             {
                 "role": "user",
                 "content": f"Here's a document: {document} \n\n---\n\n {question}",
             }
           ]
    
        # Generate an answer using the OpenAI API.
        stream = client.chat.completions.create(
              model="gpt-4.1",
              messages=messages,
              stream=True,
          )

        # Stream the response to the app using `st.write_stream`.
        st.write_stream(stream)
