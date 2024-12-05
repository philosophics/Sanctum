import os
import zipfile

# Define the source and destination directories
source_dir = "D:/_DEPLOYMENT/Raw Addon"
destination_dir = "D:/_DEPLOYMENT/Zips/"

# Ensure the destination directory exists
os.makedirs(destination_dir, exist_ok=True)

# Function to create a zip of each subdirectory, excluding specific files and directories
def create_zip_of_subdirectories():
    # List all subdirectories in the source directory
    for item in os.listdir(source_dir):
        dirpath = os.path.join(source_dir, item)

        # Skip if it's not a directory or if it's 'resources/' or 'index.html'
        if not os.path.isdir(dirpath) or item == 'resources':
            continue

        # Define the zip filename based on the subdirectory name
        zip_filename = os.path.join(destination_dir, f"{item}.zip")
        
        # Create a zip file for the directory
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(dirpath):
                # Avoid adding files in subdirectories of the targeted directory
                if root != dirpath:
                    continue
                for file in files:
                    file_path = os.path.join(root, file)
                    # Add the file to the zip (keep the directory structure relative to the source)
                    arcname = os.path.relpath(file_path, start=source_dir)
                    zipf.write(file_path, arcname)
                    
        print(f"Created zip file: {zip_filename}")

# Call the function to create zips
create_zip_of_subdirectories()