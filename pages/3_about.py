import streamlit as st
from components.disclaimer import disclaimer
from PIL import Image

image = Image.open('images/logo.png')
example = Image.open('images/example.png')



st.write("# About DocBotGPT 👋")
st.write("Experience the future of document interaction with our cutting-edge AI. Unleash the power of intelligent document analysis as our AI effortlessly sifts through your files, understanding their content. Engage in seamless conversations and unlock insights with a chat interface that allows you to ask questions and receive instant, accurate responses about your documents.")

st.markdown(
    """
     ## Example chat

    """
)

st.image(example)




st.markdown(
    """
    ### Open source
    If you're curious how this tool works, then you can. The code is [here](https://github.com/two-trick-pony-NL/DocBotGPT). 
    Feel free to open a issue or pull request with improvements. 
"""
)

st.markdown(
    """
    ### Roadmap
    This is just a MVP as proof of concept, it does not have 'users' or accounts all documents are just in 1 big pile. 
    - Register users and split each users files in their own S3 buckets
    - Provide source information (how did the LLM get it's answer)
    - Integrate with Lanchain Tools and Agents 
    - Connect up with Zapier so that the AI can execute tasks
    - Connect up to a personalised documents stores like Google Drive, Dropbox or S3
"""
)

st.markdown(
    """
    ### Contact
    - Open an issue on github [here](https://github.com/two-trick-pony-NL/DocBotGPT)
    - Send me an email docbot-fusion@petervandoorn.com
    - Or visit my website: https://petervandoorn.com
"""
)

st.write("---")
st.write("*Note: This tool heavily uses a Large Language Model, and while impressive: might not always produce accurate answers. See full disclaimer.*")


with st.expander("⚠️ Disclaimer"):
    disclaimer()
    
