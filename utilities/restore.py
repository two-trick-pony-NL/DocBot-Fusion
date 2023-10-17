import os
import shutil

def demo_data():
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
        
        
def reset_instructions():
    folder_name = 'data'
    file_name = 'instructions.txt'
    file_content = 'Write a prompt to get started'

    # Create the 'data' folder
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Create and write to the 'instructions.txt' file
    file_path = os.path.join(folder_name, file_name)
    with open(file_path, 'w') as file:
        file.write(file_content)

    print(f'The folder "{folder_name}" and file "{file_name}" have been created.')