import streamlit as st


st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Streamlit! 👋")

st.sidebar.title('🔥Docusearch GPT App')
st.sidebar.write(
    "This app combines ChatGPT's conversational abilities with document analysis. "
    "It processes uploaded documents, extracting insights and generating contextually relevant responses. "
    "The result is a powerful tool for both casual conversations and professional tasks."
)



st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)

with st.expander("⚠️ Disclaimer"):
    st.write("This app may produce inaccurate information - it derives it's answers from Statistics and thus will give the most probable answer, not necessary a factual one. ")
