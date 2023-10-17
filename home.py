import streamlit as st
import os


from components.sidebar import sidebar_component
st.set_page_config(
    page_title=" DocBot Fusion", 
    layout="wide",
    page_icon='💬',
    initial_sidebar_state='expanded',
    menu_items={
        'Report a bug': "https://github.com/two-trick-pony-NL/DocBot-Fusion/issues",
        'About': "https://petervandoorn.com"
    })



sidebar_component()
st.balloons()



from PIL import Image

image = Image.open('images/logo.png')
example = Image.open('images/example.png')


#st.image(image)

st.markdown(
    """
    # If ChatGPT really knew you, what would it say? 😏
    Well you're about to find out. With Docbot Fusion you fuse ChatGPT with **your** files so that it knows what's going on in your life.""")

# Place buttons in the columns
st.markdown('<a href="/chat" target="_self">Start Chat 💬 </a>', unsafe_allow_html=True)
st.markdown('<a href="/files" target="_self">Upload files 🗂️ </a>', unsafe_allow_html=True)

st.markdown("""
    ## How does that work? Simple:
    - 📤 just upload some files like your calendar 📆 and preferences of your family 👨‍👩‍👧
    
    - 💬 Start chatting
    - 🤓 Get personalsid responses
    
"""
)
