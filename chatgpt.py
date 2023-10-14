import streamlit as st
import os
import sys

import openai
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma

import constants

os.environ["OPENAI_API_KEY"] = constants.APIKEY

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = True

# List files in the "data" folder
data_folder = "data"
data_files = [file for file in os.listdir(data_folder) if os.path.isfile(os.path.join(data_folder, file))]

#Title
st.title('🔥Docusearch GPT App')
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []



# Sidebar to display files
st.sidebar.title("File List")
st.sidebar.write(data_files)
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Set a larger text input box
query = st.chat_input("What do you want to know?:")
if query:
    with st.chat_message("user"):
        st.markdown(query)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": query})

    if PERSIST and os.path.exists("persist"):
        print("Reusing index...\n")
        vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
        index = VectorStoreIndexWrapper(vectorstore=vectorstore)
    else:
        loader = DirectoryLoader(data_folder)
        if PERSIST:
            index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory": "persist"}).from_loaders([loader])
        else:
            index = VectorstoreIndexCreator().from_loaders([loader])

    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model="gpt-3.5-turbo"),
        retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
    )

    chat_history = []
    if query:
        result = chain({"question": query, "chat_history": chat_history})
        chat_history.append((query, result['answer']))
        with st.chat_message("assistant"):
          st.markdown(result["answer"])
          # Add assistant response to chat history
          st.session_state.messages.append({"role": "assistant", "content": result["answer"]})
