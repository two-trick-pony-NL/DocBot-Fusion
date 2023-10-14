import streamlit as st
import os
import time
import constants

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.vectorstores import Chroma

os.environ["OPENAI_API_KEY"] = constants.APIKEY

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = True

# List files in the "data" folder
data_folder = "data"
data_files = [file for file in os.listdir(data_folder) if os.path.isfile(os.path.join(data_folder, file))]
previous_data_files = data_files.copy()
# Check if new files were uploaded



# Title
st.title('🔥Docusearch GPT App')
with st.expander("⚠️ Disclaimer"):
    st.write("This is a AI model, it creates answers on a best effort basis using Statistics. This does not ensure all information is alway 100 percent factual. As a result it's advices to always think and verify before assumgin any information given by the AI is true. ")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar to display files and allow document upload
st.sidebar.title("File List and Upload")
uploaded_files = st.sidebar.file_uploader("Upload documents", accept_multiple_files=True)
    
for uploaded_file in uploaded_files or []:
    with open(os.path.join(data_folder, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getvalue())
    data_files.append(uploaded_file.name)

st.sidebar.write("Available files:")
st.sidebar.write(data_files)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Set a larger text input box
query = st.chat_input("What do you want to know?")
if not query:
    st.success("Ask a question in the chatbox to get started!")
if query:
    with st.spinner("Thinking..."):
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
            llm=ChatOpenAI(model="gpt-3.5-turbo", cache=False),
            retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
        )

        chat_history = []
        if query:
            result = chain({"question": query, "chat_history": chat_history})
            chat_history.append((query, result['answer']))
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                assistant_response = result["answer"]

                # Simulate stream of response with milliseconds delay
                for chunk in assistant_response.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": result["answer"]})