import os
import streamlit as st
import time
from langchain.globals import set_llm_cache
from langchain.cache import InMemoryCache
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.vectorstores import Chroma
import json
from utilities.find_common_words import find_common_words
from utilities.file_upload import save_uploaded_file
from components.disclaimer import disclaimer

# Set OpenAI and Zapier API key from Streamlit secrets
os.environ["OPENAI_API_KEY"] = st.secrets.APIKEY
# Enable to save to disk & reuse the model (for repeated queries on the same data)
# Can't persist for now as Streamlit does not support the sqlite database
PERSIST = True

# Create an instance of InMemoryCache
llm_cache = InMemoryCache()
# Set the llm_cache using set_llm_cache function
set_llm_cache(llm_cache)

from PIL import Image
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import sqlite3

# Load the app logo
image = Image.open('images/logo.png')
st.sidebar.image(image)


# List files in the "data" folder
data_folder = "data"
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

    
        
#Adding file upload
uploaded_file = st.sidebar.file_uploader("", type=['pdf', 'txt'], accept_multiple_files=True)
save_uploaded_file(uploaded_file, data_folder)


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat_history = []




# Display file contents
st.header("💬 Chat")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Set a larger text input box
query = st.chat_input("What do you want to know?", max_chars=500)
if not query:
    # Create three buttons in a row
    col1, col2, col3 = st.columns(3)
    # Place buttons in the columns
    button1 = col1.button('📆 What is my schedule tomorrow?')
    button2 = col2.button('🏢 What companies did I work for?')
    button3 = col3.button('💳 what was a expensive recent purchase?')
    # Define behavior when buttons are clicked
    if button1:
        query = "What is my schedule tomorrow?"
    if button2:
        query = "What companies did I work for?"
    if button3:
        query = "what was the most expensive thing I bought recently?"

    # Additional suggestions in the sidebar
    st.sidebar.write(
    "Start chatting with your personal assistant, if you don't know what to talk about then here are some ideas: "
)
    if st.sidebar.button('👨🏻‍🍳 Do I have time to cook a big meal tomorrow? ', key='suggestion1'):
        query = "Do I have time to cook a big meal tomorrow?"
    if st.sidebar.button('🏆 Tell me 3 of my strengths 🏆', key='suggestion2'):
        query = "Given my work experience on LinkedIn, samenvatting, Publications, ervaring, Belangrijkste vaardigheden,  education, opleiding could you tell me 3 of my strengths??"
    if st.sidebar.button('💸 What should I cut back on with Spending? ', key='suggestion3'):
        query = "What should I cut back spending on?"
    if st.sidebar.button('🍿 What movie should I watch with my family tonight? ', key='suggestion4'):
        query = "Based on my family composition of wife and young daughter, suggest 3 movie ideas for tonight?"

# Chat with the assistant based on user input
if query:
    chat_history = st.session_state.chat_history
    with st.spinner("Hang on..."):
        with st.chat_message("user"):
            st.markdown(query)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": query})

        

        # Initialize the ConversationalRetrievalChain
        if PERSIST and os.path.exists("persist"):
            print("Reusing index...\n")
            vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
            index = VectorStoreIndexWrapper(vectorstore=vectorstore)
        else:
            loader = DirectoryLoader(data_folder)
            if PERSIST:
                index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory": "persist"}).from_loaders(
                    [loader]
                )
            else:
                index = VectorstoreIndexCreator().from_loaders([loader])
            
        chain = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(
                model="gpt-3.5-turbo", 
                cache=True, temperature=1.3), 
            return_source_documents=True,

            # See documentation on retrievers: https://python.langchain.com/docs/modules/data_connection/retrievers/vectorstore 
            #retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
            #retriever=index.vectorstore.as_retriever(search_kwargs={"k": 3}),
            retriever=index.vectorstore.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": .3})
            #retriever=index.vectorstore.as_retriever(search_type="mmr")



        )

        # Chat with the assistant and display the response
        if query:
            result = chain({"question": query, "chat_history": chat_history})
            try:
                with st.expander("ℹ️ Source"):
                        document = result["source_documents"][0]
                        print("##### DOCUMETN ####")
                        print(document)
                        # Extracting page content and metadata
                        page_content = str(document.page_content)
                        metadata = str(document.metadata)
                        data_dict = json.loads(metadata.replace("'", "\""))
                        source_value = data_dict['source']
                        st.markdown(f"### {source_value}")
                        st.markdown(find_common_words(page_content, query))
            except:
                print("no source")

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
    # Save the updated chat history back to session state
    st.session_state.chat_history = chat_history


# Display disclaimers in the sidebar expander
with st.sidebar.expander("⚠️ Disclaimer"):
    disclaimer()
    