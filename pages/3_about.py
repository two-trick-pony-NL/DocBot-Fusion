import streamlit as st
from PIL import Image
from utilities.metrics import *
from components.disclaimer import disclaimer
import pandas as pd

add_pageview_row(1)

image = Image.open('images/logo.png')

st.sidebar.image(image)


st.write("# About DocBotGPT 👋")
st.write("Experience the future of document interaction with our cutting-edge AI. Unleash the power of intelligent document analysis as our AI effortlessly sifts through your files, understanding their content. Engage in seamless conversations and unlock insights with a chat interface that allows you to ask questions and receive instant, accurate responses about your documents.")

st.markdown(
    """
     ## Example chat

    """
)





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

# Load the app logo

st.title("Analytics 📈")
st.write("Some simple metrics on a dashboard to see how many people use the bot")

col1, col2, col3 = st.columns(3)

# Total Questions Metric
questions_df = read_csv_to_df('questions.csv')
questions_df['timestamp'] = pd.to_datetime(questions_df['timestamp'])
questions_df.set_index('timestamp', inplace=True)  # Set timestamp as index
total_questions = questions_df['question_count'].sum()
last_question_timestamp = questions_df.index.max()
col1.metric("Total Questions Answered", f"{total_questions}", f"Last Question: {last_question_timestamp}")

# Total Files Metric
files_df = read_csv_to_df('files.csv')
files_df['timestamp'] = pd.to_datetime(files_df['timestamp'])
files_df.set_index('timestamp', inplace=True)  # Set timestamp as index
total_files_uploaded = files_df['upload_count'].sum()
last_file_timestamp = files_df.index.max()
col2.metric("Total Files Uploaded", f"{total_files_uploaded}", f"Last Upload: {last_file_timestamp}")

# Total Page Views Metric
pageviews_df = read_csv_to_df('pageviews.csv')
pageviews_df['timestamp'] = pd.to_datetime(pageviews_df['timestamp'])
pageviews_df.set_index('timestamp', inplace=True)  # Set timestamp as index

# Resample pageviews data to 30-minute intervals
pageviews_resampled = pageviews_df.resample('H').count()

total_pageviews = pageviews_df['pageview_count'].sum()
last_pageview_timestamp = pageviews_df.index.max()
col3.metric("Total Page Views", f"{total_pageviews}", f"Last Page View: {last_pageview_timestamp}")

# Create bar charts showing usage over time for questions, files, and page views
st.subheader("Questions Over Time")

# Resample questions data to 30-minute intervals
questions_resampled = questions_df.resample('H').count()

# Questions Over Time
st.bar_chart(questions_resampled['question_count'])

# Files Over Time
st.subheader("File uploads Over Time")
files_resampled = files_df.resample('H').sum()  # Adjust 'sum()' to your desired aggregation
st.bar_chart(files_resampled['upload_count'])

# Page Views Over Time
st.subheader("Page Views Over Time")
st.bar_chart(pageviews_resampled['pageview_count'])

with st.expander("⚠️ Disclaimer"):
    disclaimer()