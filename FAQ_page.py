import streamlit as st
import pandas as pd
import langchain 
#from openai import OpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.document_loaders import DataFrameLoader
from langchain_core.vectorstores import InMemoryVectorStore


llm = ChatOpenAI()

# Show title and description.
st.title("📄 Тестируем FAQ")
#st.write(
#    "Upload a document below and ask a question about it – GPT will answer! "
openai_api_key = st.secrets["OPENAI_API_KEY"]
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)
#    embeddings_ai = client.embeddings.create(input = "Test", model="text-embedding-3-small")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    model = st.selectbox(
      "Выберите ИИ модель:",
      ("gpt-4.1", "o4-mini", "gpt-4o"),
    )
# Форма для ввода пар вопросов и ответов
    with st.form("qa_form"):
       st.write("Заведите свои ЧаВо")
       df = pd.DataFrame(
           [
              {"Question": "Что?", "Answer": "Streamlit"},
              {"Question": "Где?", "Answer": "Здесь"},
              {"Question": "Когда?", "Answer": "Сейчас"},
          ]
       )
       edited_df = st.data_editor(df)
       query = st.text_input("Задайте вопрос по FAQ:", "") 
       qa_submitted = st.form_submit_button("Отправить") 
       loader = DataFrameLoader(
           data_frame = edited_df,
           page_content_column = "Question"
        )
    if qa_submitted:
       documents = loader.load()
#       st.write(documents)
       text_splitter = RecursiveCharacterTextSplitter(
       chunk_size=1000, chunk_overlap=200, add_start_index=True
       )
       all_splits = text_splitter.split_documents(documents)
 
       vector_store = InMemoryVectorStore(embeddings)
       ids = vector_store.add_documents(documents=all_splits)
       retriever = vector_store.as_retriever() 
#       results1 = vector_store.similarity_search("www?")
#       st.write("results1:")
#       st.write(results1[0])
# --------------------------------------
       system_prompt = (
         "Use the given context to answer the question. "
         "If you don't know the answer, say you don't know. "
         "Use three sentence maximum and keep the answer concise. "
         "Context: {context}"
       )
       prompt = ChatPromptTemplate.from_messages(
         [
           ("system", system_prompt),
           ("human", "{input}"),
         ]
       )
       question_answer_chain = create_stuff_documents_chain(llm, prompt)
       chain = create_retrieval_chain(retriever, question_answer_chain)
       chain.invoke({"input": query}) 
       chain.save(file_path="chain.yaml") 
 # -------------------       
       results = vector_store.similarity_search_with_score(query)
           #print(results[0])
       doc, score = results[0]
       answer = doc.metadata
       st.write(f"Score: {score}\n")
       st.write(doc)
       st.write(answer) 

