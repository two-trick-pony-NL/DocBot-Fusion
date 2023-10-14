

import streamlit as st
from PIL import Image

def sidebar_component():

    image = Image.open('images/logo.png')
    st.sidebar.image(image)
    st.sidebar.title('DocBot Fusion')
    st.sidebar.write(
        "This app combines ChatGPT's conversational abilities with document analysis. "
        "It processes uploaded documents, extracting insights and generating contextually relevant responses. "
        "The result is a powerful tool for both casual conversations and professional tasks."
    )

    with st.sidebar.expander("⚠️ Disclaimer"):
        st.write("This app may produce inaccurate information - it derives it's answers from Statistics and thus will give the most probable answer, not necessary a factual one. ")



