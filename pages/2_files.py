import streamlit as st
import os
import pandas as pd
from PIL import Image
from utilities.restore import demo_data
from utilities.delete import delete_data_folder, delete_persistence
from utilities.file_upload import save_uploaded_file
from components.disclaimer import disclaimer
from utilities.metrics import *
add_pageview_row(1)


image = Image.open('images/logo.png')
st.sidebar.image(image)

# Restore button
if st.sidebar.button("Use Demo Files", key='restore', type="primary", use_container_width=True):
    print('restore function')
    delete_persistence() # Deleting all we know
    demo_data() #setting demo data

# Deletion button
if st.sidebar.button("Delete all files", key='delete', use_container_width=True):
    delete_data_folder()
    st.success("Files deleted successfully!")


st.sidebar.title('If chatGPT could read your documents, what would it say?')
st.sidebar.write(
    "The more documents you upload the better responses we'll generate. Here are some ideas of documents you could upload: "
)
categories = [
    ("Calendar/Appointment Book", "Reveals scheduled events, meetings, and commitments."),
    ("Contacts List", "Includes names, phone numbers, and email addresses of people the person is in contact with."),
    ("Bank Statements", "Details financial transactions, income, expenses, and spending patterns."),
    ("Resume/CV", "Provides information about education, work experience, skills, and qualifications."),
    ("Social Media Profiles", "Gives insights into personal interests, social connections, and online activities."),
    ("Medical Records", "Contains information about health conditions, medications, and medical history."),
    ("Utility Bills", "Reflects the person's address, living situation, and usage patterns."),
    ("Tax Returns", "Provides information about income, deductions, and financial obligations."),
    ("Emails", "Communication history, including both personal and professional conversations."),
    ("Travel Records", "Reveals places visited, travel patterns, and frequency of travel."),
    ("Property Deeds/Leases", "Indicates home ownership or rental history."),
    ("Legal Documents (e.g., Contracts, Wills)", "Offers insights into legal obligations, agreements, and intentions."),
    ("Education Certificates/Transcripts", "Highlights academic achievements, courses taken, and educational background."),
    ("Insurance Policies", "Outlines types of insurance coverage, beneficiaries, and policy details."),
    ("Memberships/Subscriptions", "Shows affiliations with organizations, clubs, or subscription services."),
    ("Personal Journals/Diaries", "Offers personal reflections, thoughts, and experiences.")
]

with st.sidebar:
    for title, content in categories:
        with st.expander(title):
            st.write(content)

# Set up your Streamlit app
st.header("🗂️ Your files")

# Create a folder if it doesn't exist
data_folder = 'data'
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# List of uploaded files
uploaded_files_list = os.listdir(data_folder)



# Call the function to save the uploaded file
uploaded_file = st.file_uploader("", type=['pdf', 'txt'], accept_multiple_files=True)
save_uploaded_file(uploaded_file, data_folder)

# Display file content if a file is selected
if st.button("Use Demo Files", key='restorebig', type="primary", use_container_width=True):
    print('restore function')
    delete_persistence() # Deleting all we know
    demo_data() #setting demo data

# Deletion button
if st.button("Delete all files", key='deletebig', use_container_width=True):
    delete_data_folder()
    st.success("Files deleted successfully!")
selected_file = st.selectbox("Select File to Preview", uploaded_files_list)
# Restore button



# Display file content if a file is selected
if selected_file:
    file_path = os.path.join(data_folder, selected_file)
    file_extension = selected_file.split('.')[-1]
    
    if file_extension.lower() == 'csv':
        df = pd.read_csv(file_path)
        st.write("### Preview of Selected CSV File")
        st.write(df)
    elif file_extension.lower() == 'txt' or file_extension.lower() == 'py':
        with open(file_path, 'r') as file:
            text_content = file.read()
            st.write("### Preview of Selected Text File")
            st.text(text_content)
    else:
        st.warning("Preview not available for this file type.")

# Disclaimer section
with st.sidebar.expander("⚠️ Disclaimer"):
    disclaimer()
    
