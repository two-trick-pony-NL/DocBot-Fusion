import streamlit as st
import os
import pandas as pd
from PIL import Image

image = Image.open('images/logo.png')
st.sidebar.image(image)

# Set up your Streamlit app
st.header("🗂️ Your files")


# Create a folder if it doesn't exist
data_folder = 'data'
if not os.path.exists(data_folder):
    os.makedirs(data_folder)




# List of uploaded files
uploaded_files_list = os.listdir(data_folder)

st.write("### 🔎 Stored Files")
st.write("DocBot keeps track of the contents of these files to understand you better. It will use information in these files in its responses to you.")
if uploaded_files_list:
    for file_name in uploaded_files_list:
        st.write("-", file_name)
else:
    st.warning("No files uploaded yet.")
    
# Upload files
st.write("### 📤 Upload Files")
st.write("Simply add more documents to DocBot and it will better learn about your life")
uploaded_files = st.file_uploader("", type=['pdf', 'txt'])

st.write("### 📄 Document inspector")
st.write("Here you can see the contents of the documents you have already uploaded")
selected_file = st.selectbox("Select File to Preview", uploaded_files_list)


# Display file content if a file is selected
if selected_file:
    file_path = os.path.join(data_folder, selected_file)
    file_extension = selected_file.split('.')[-1]
    
    if file_extension.lower() == 'csv':
        df = pd.read_csv(file_path)
        st.write("### Preview of Selected CSV File")
        st.write(df)
    elif file_extension.lower() == 'txt':
        with open(file_path, 'r') as file:
            text_content = file.read()
            st.write("### Preview of Selected Text File")
            st.text(text_content)
    else:
        st.warning("Preview not available for this file type.")

