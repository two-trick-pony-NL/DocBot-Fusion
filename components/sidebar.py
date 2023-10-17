

import streamlit as st


def sidebar_component():
    from PIL import Image
    image = Image.open('images/logo.png')
    st.sidebar.image(image)
    st.sidebar.title('DocBot Fusion')
    st.sidebar.write(
        "This app combines ChatGPT's conversational abilities with document analysis. "
        "It processes uploaded documents, extracting insights and generating contextually relevant responses. "
        "The result is a powerful tool for both casual conversations and professional tasks."
    )



