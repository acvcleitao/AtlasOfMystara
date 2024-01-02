import os

def delete_md_files(folder_path):
    try:
        # Walk through the directory tree
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                # Check if the file has a .md extension
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    # Delete the file
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")

        print("Deletion of .md files completed.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Specify the path of the root folder
root_folder_path = "PoC\Database"

# Call the function to delete .md files recursively
delete_md_files(root_folder_path)
