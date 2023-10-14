# Import necessary libraries
import os
import streamlit as st
import time
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.vectorstores import Chroma
from langchain.cache import InMemoryCache

set_llm_cache(InMemoryCache())

from PIL import Image
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import sqlite3

# Load the app logo
image = Image.open('images/logo.png')
st.sidebar.image(image)

# Set OpenAI API key from Streamlit secrets
os.environ["OPENAI_API_KEY"] = st.secrets.APIKEY

# Enable to save to disk & reuse the model (for repeated queries on the same data)
# Can't persist for now as Streamlit does not support the sqlite database
PERSIST = True

# List files in the "data" folder
data_folder = "data"
data_files = [file for file in os.listdir(data_folder) if os.path.isfile(os.path.join(data_folder, file))]
previous_data_files = data_files.copy()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display title and introductory message
st.sidebar.title('If chatGPT really knew you, what would it say?')
st.sidebar.write(
    "Start chatting with your personal assistant, if you don't know what to talk about then here are some ideas: "
)

# Display file contents
st.header("💬 Chat")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Set a larger text input box
query = st.chat_input("What do you want to know?")
if not query:
    st.success("Ask a question in the chatbox to get started!")
    # Create three buttons in a row
    col1, col2, col3 = st.columns(3)
    # Place buttons in the columns
    button1 = col1.button('What is my schedule tomorrow?')
    button2 = col2.button('What companies did I work for?')
    button3 = col3.button('what was a expensive recent purchase?')
    # Define behavior when buttons are clicked
    if button1:
        query = "What is my schedule tomorrow?"
    if button2:
        query = "What companies did I work for?"
    if button3:
        query = "what was the most expensive thing I bought recently?"

    # Additional suggestions in the sidebar
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
            llm=ChatOpenAI(model="gpt-3.5-turbo", cache=True, temperature=1.2),
            retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
        )

        # Chat with the assistant and display the response
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

# Display disclaimers in the sidebar expander
with st.sidebar.expander("⚠️ Disclaimer"):
    st.write("""
             ### AI is just statistics, it can't really think and thus can't be trusted to tell the truth
             This site may produce inaccurate information - Generative AI Is just fancy statistics. So in a clever way all the words you see generated are just the most probable next words. Without basing them in any facts. Always use your own judgement when reading the results from this AI.  """)
    st.write("""
    ### Privacy Disclaimer

    **Your Choices Matter:**
    This app allows you to upload and preview personal documents. Be mindful of the information you choose to share. Only upload and interact with documents that you are comfortable sharing, and always consider the privacy implications.

    **Sensitive Information:**
    Avoid uploading sensitive or confidential information unless necessary. Understand that the app processes information for display purposes only and doesn't store or transmit your data.

    **Your Responsibility:**
    You are responsible for the documents you choose to upload. Ensure you comply with privacy laws and regulations. Be cautious about sharing personally identifiable information.

    **Security Measures:**
    While we take measures to ensure the security of the app, there is always a risk associated with online interactions. Use the app in a secure and private environment.

    **Questions or Concerns:**
    If you have questions or concerns about privacy, feel free to reach out to us.

    """)
    st.write("""
    ### No Responsibility Disclaimer

    **Use at Your Own Risk:**
    This app is provided as-is, and we do not guarantee the accuracy or completeness of the information it produces. The app generates answers based on statistical data and may not always provide factual information.

    **Limitation of Liability:**
    We disclaim any responsibility for the consequences of using this app. The information provided is for informational purposes only, and we do not accept any liability for actions taken based on the app's outputs.

    **User Responsibility:**
    You, as the user, are solely responsible for the choices you make based on the information generated by the app. Verify critical information independently before making decisions.

    **No Warranty:**
    We make no warranties, expressed or implied, regarding the app's functionality, accuracy, or fitness for a particular purpose.

    **Changes and Updates:**
    We may update or modify the app without notice, and we are not obligated to provide support or updates.

    **Questions or Concerns:**
    If you have any questions or concerns, please contact us.

    """)
