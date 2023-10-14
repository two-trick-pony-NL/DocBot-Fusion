import streamlit as st
#from components.logo import logo_component
from components.sidebar import sidebar_component
#logo_component()
sidebar_component()

st.markdown(
    """
    # Welcome to Docbot Fusion 👋🏻
    If ChatGPT would really know **you**, what would it say? Well you're about to find out. With Docbot Fusion you fuse ChatGPT with **your** files so that it knows what's going on in your life. 
    
    ## How does that work? 
    Simple: just upload some files, your calendar your favourite recipes and start asking questions: 
    - What should I eat today
    - 
    
    
    ## Get started 
   
"""
)

# Place buttons in the columns
st.markdown('<a href="/chat" target="_self">Start Chat 💬 </a>', unsafe_allow_html=True)
st.markdown('<a href="/files" target="_self">Upload files 🗂️ </a>', unsafe_allow_html=True)


st.markdown(
    """
    ### Open source
    If you're curious how this tool works, then you can. The code is [here](https://github.com/two-trick-pony-NL/DocBot-Fusion)
"""
)

with st.expander("⚠️ Disclaimer and Privacy"):
    st.write("This app may produce inaccurate information - it derives it's answers from Statistics and thus will give the most probable answer, not necessary a factual one. ")
