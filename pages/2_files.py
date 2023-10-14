import streamlit as st
import os
import pandas as pd
from PIL import Image

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


with st.sidebar.expander("⚠️ Disclaimer"):
    st.write("""
             ### AI is just statistics, it can't really think and thus can't be trusted to tell the truth
             This site may produce inaccurate information - Generative AI Is just fancy statistics. So in a clever way all the words you see generated are just the most probable next words. Without basing them in any facts. Always use your own judgement when reading the results from this AI.  """)
    st.write("""
    ### Privacy Disclaimer

    **Your Choices Matter:**
    This app allows you to upload and preview personal documents. Be mindful of the information you choose to share. Only upload and interact with documents that you are comfortable sharing, and always consider the privacy implications.

    **Sensitive Information:**
    Avoid uploading sensitive or confidential information unless necessary. Understand that the app processes information for display purposes only and doesn't store or transmit your data.

    **Your Responsibility:**
    You are responsible for the documents you choose to upload. Ensure you comply with privacy laws and regulations. Be cautious about sharing personally identifiable information.

    **Security Measures:**
    While we take measures to ensure the security of the app, there is always a risk associated with online interactions. Use the app in a secure and private environment.

    **Questions or Concerns:**
    If you have questions or concerns about privacy, feel free to reach out to us.

    """)
    st.write("""
    ### No Responsibility Disclaimer

    **Use at Your Own Risk:**
    This app is provided as-is, and we do not guarantee the accuracy or completeness of the information it produces. The app generates answers based on statistical data and may not always provide factual information.

    **Limitation of Liability:**
    We disclaim any responsibility for the consequences of using this app. The information provided is for informational purposes only, and we do not accept any liability for actions taken based on the app's outputs.

    **User Responsibility:**
    You, as the user, are solely responsible for the choices you make based on the information generated by the app. Verify critical information independently before making decisions.

    **No Warranty:**
    We make no warranties, expressed or implied, regarding the app's functionality, accuracy, or fitness for a particular purpose.

    **Changes and Updates:**
    We may update or modify the app without notice, and we are not obligated to provide support or updates.

    **Questions or Concerns:**
    If you have any questions or concerns, please contact us.

    """)


