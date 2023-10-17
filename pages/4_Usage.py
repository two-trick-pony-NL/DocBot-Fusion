import streamlit as st
from PIL import Image
from utilities.metrics import *
add_pageview_row(1)

# Load the app logo
image = Image.open('images/logo.png')
st.image(image)

st.title("Analytics 📈")
st.write("Some simple metrics on a dashboard to see how many people use the bot")

col1, col2, col3 = st.columns(3)

# Total Questions Metric
total_questions = read_csv_to_df('questions.csv')['question_count'].sum()
last_question_timestamp = read_csv_to_df('questions.csv')['timestamp'].max()
col1.metric("Total Questions Answered", f"{total_questions}", f"Last Question: {last_question_timestamp}")

# Total Files Metric
files_df = read_csv_to_df('files.csv')
total_files_uploaded = files_df['upload_count'].sum()
last_file_timestamp = files_df['timestamp'].max()
col2.metric("Total Files Uploaded", f"{total_files_uploaded}", f"Last Upload: {last_file_timestamp}")

# Total Page Views Metric
pageviews_df = read_csv_to_df('pageviews.csv')
total_pageviews = pageviews_df['pageview_count'].sum()
last_pageview_timestamp = pageviews_df['timestamp'].max()
col3.metric("Total Page Views", f"{total_pageviews}", f"Last Page View: {last_pageview_timestamp}")

# Create bar charts showing usage over time for questions, files, and page views
st.subheader("Usage Over Time")

# Questions Over Time
st.bar_chart(read_csv_to_df('questions.csv').set_index('timestamp'))

# Files Over Time
st.bar_chart(files_df.set_index('timestamp'))

# Page Views Over Time
st.bar_chart(pageviews_df.set_index('timestamp'))
