
import streamlit as st
import os
import time
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.vectorstores import Chroma

os.environ["OPENAI_API_KEY"] = st.secrets.APIKEY

# Enable to save to disk & reuse the model (for repeated queries on the same data)
#Can't persist for now as Streamlit does not support the sqlite database
PERSIST = False

# List files in the "data" folder
data_folder = "data"
data_files = [file for file in os.listdir(data_folder) if os.path.isfile(os.path.join(data_folder, file))]
previous_data_files = data_files.copy()
# Check if new files were uploaded



# Title
st.sidebar.title('🔥Docusearch GPT App')
st.sidebar.write("This app combines ChatGPT's conversational abilities with document analysis. It processes uploaded documents, extracting insights and generating contextually relevant responses. The result is a powerful tool for both casual conversations and professional tasks.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar to display files and allow document upload
st.sidebar.header("File List and Upload")
uploaded_files = st.sidebar.file_uploader("Upload documents", accept_multiple_files=True)

# Display uploaded files and preview their content
st.sidebar.write("Available files:")
st.sidebar.write(data_files)

for uploaded_file in uploaded_files or []:
    with open(os.path.join(data_folder, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getvalue())
    data_files.append(uploaded_file.name)

# Display file contents
st.header("Preview of Uploaded Files")

# Modal window to display file content
selected_file = st.sidebar.selectbox("Select a file to preview:", data_files)
if selected_file:
    file_path = os.path.join(data_folder, selected_file)
    file_contents = ""
    with open(file_path, "r") as file:
        file_contents = file.read()

    # Button to open modal
    if st.sidebar.button(f"Preview {selected_file}"):
        st.markdown(f"### Previewing {selected_file}")
        st.text(file_contents)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Set a larger text input box
query = st.chat_input("What do you want to know?")
if not query:
    st.success("Ask a question in the chatbox to get started!")
if query:
    with st.spinner("Hang on..."):
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