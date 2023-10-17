import os
import shutil
from .restore import reset_instructions

def delete_data_folder():
    folder_path = 'data'

    # Check if the folder exists
    if os.path.exists(folder_path):
        try:
            # Remove the folder and its contents
            shutil.rmtree(folder_path)
            print(f"The folder '{folder_path}' has been successfully deleted.")
            reset_instructions()
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"The folder '{folder_path}' does not exist.")
    delete_persistence()
        
        
def delete_persistence():
    folder_path = 'persist'

    # Check if the folder exists
    if os.path.exists(folder_path):
        try:
            # Remove the folder and its contents
            shutil.rmtree(folder_path)
            print(f"The folder '{folder_path}' has been successfully deleted.")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"The folder '{folder_path}' does not exist.")