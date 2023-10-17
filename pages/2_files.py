import streamlit as st
import os
import pandas as pd
from PIL import Image
import time
import shutil


image = Image.open('images/logo.png')
st.sidebar.image(image)

st.sidebar.title('If chatGPT really knew you, what would it say?')
st.sidebar.write(
    "The more documents you upload the better responses we'll generate. Here are some ideas of documents you could upload: "
)
st.sidebar.markdown(
    """
    - **Calendar/Appointment Book:**
  - Reveals scheduled events, meetings, and commitments.

- **Contacts List:**
  - Includes names, phone numbers, and email addresses of people the person is in contact with.

- **Bank Statements:**
  - Details financial transactions, income, expenses, and spending patterns.

- **Resume/CV:**
  - Provides information about education, work experience, skills, and qualifications.

- **Social Media Profiles:**
  - Gives insights into personal interests, social connections, and online activities.

- **Medical Records:**
  - Contains information about health conditions, medications, and medical history.

- **Utility Bills:**
  - Reflects the person's address, living situation, and usage patterns.

- **Tax Returns:**
  - Provides information about income, deductions, and financial obligations.

- **Emails:**
  - Communication history, including both personal and professional conversations.

- **Travel Records:**
  - Reveals places visited, travel patterns, and frequency of travel.

- **Property Deeds/Leases:**
  - Indicates home ownership or rental history.

- **Legal Documents (e.g., Contracts, Wills):**
  - Offers insights into legal obligations, agreements, and intentions.

- **Education Certificates/Transcripts:**
  - Highlights academic achievements, courses taken, and educational background.

- **Insurance Policies:**
  - Outlines types of insurance coverage, beneficiaries, and policy details.

- **Memberships/Subscriptions:**
  - Shows affiliations with organizations, clubs, or subscription services.

- **Personal Journals/Diaries:**
  - Offers personal reflections, thoughts, and experiences.

   
    
   
"""
)

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
    
# Deletion button
if st.button("Delete file", key='delete'):
    print('delete function')
    st.success("Files deleted successfully!")
    folder_path = os.path.join(os.path.dirname(__file__), '..', 'data')

    # Check if the folder exists
    if os.path.exists(folder_path):
        try:
            # Remove the folder and its contents
            shutil.rmtree(folder_path)
            print(f"The folder '{folder_path}' has been successfully deleted.")
            st.rerun()
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"The folder '{folder_path}' does not exist.")


def is_data_folder_empty():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data')
    return not os.listdir(data_path)

# Restore button

if st.button("Use Demo Files", key='restore'):
    print('restore function')
    backup_path = os.path.join(os.path.dirname(__file__), '..', 'backup')
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data')

    # Check if the backup folder exists
    if os.path.exists(backup_path):
        try:
            # If the data folder exists, remove it
            if os.path.exists(data_path):
                shutil.rmtree(data_path)

            # Copy the contents of the backup folder to the data folder
            shutil.copytree(backup_path, data_path)
            print(f"Contents of '{backup_path}' successfully copied to '{data_path}'.")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"The folder '{backup_path}' does not exist.")


# Upload files
st.write("### 📤 Upload Files")
st.write("Simply add more documents to DocBot and it will better learn about your life")
uploaded_file = st.file_uploader("", type=['pdf', 'txt'])

# Save uploaded files to disk
if uploaded_file is not None:
    # Use the original filename
    file_name = str(uploaded_file.name)
    file_path = os.path.join(data_folder, file_name)

    # Save the file to disk
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getvalue())

    st.success(f"File '{file_name}' uploaded successfully!")

# Display file content if a file is selected
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

# Disclaimer section
with st.sidebar.expander("⚠️ Disclaimer"):
    st.write("""
             ### AI is just statistics, it can't really think and thus can't be trusted to tell the truth
             This site may produce inaccurate information - Generative AI Is just fancy statistics. So in a clever way all the words you see generated are just the most probable next words. Without basing them in any facts. Always use your own judgement when reading the results from this AI.  """)
    st.write("""
    ### Privacy Disclaimer

    **Your Choices Matter:**
    This app allows you to upload and preview personal documents. Be mindful of the information you choose to share. Only upload and interact with documents that you are comfortable sharing, and always consider the privacy implications.

    ...
    """)
    st.write("""
    ### No Responsibility Disclaimer

    **Use at Your Own Risk:**
    This app is provided as-is, and we do not guarantee the accuracy or completeness of the information it produces. The app generates answers based on statistical data and may not always provide factual information.

    ...
    """)
