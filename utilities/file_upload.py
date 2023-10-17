import os
import streamlit as st
from .delete import delete_persistence
from .metrics import *


def save_uploaded_file(uploaded_files, data_folder):
    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_name = str(uploaded_file.name)
            file_path = os.path.join(data_folder, file_name)
            add_file_row(1)

            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getvalue())

            # By deleting the persistence, you force a revectorization of your files
            delete_persistence()
            
            st.success(f"File '{file_name}' uploaded successfully!")
    else:
        st.warning("Upload some files to get personalised answers.")
