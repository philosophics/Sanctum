import os
import shutil
import zipfile
from datetime import datetime

# Define source and destination paths
source_dir = "C:/Users/philo/AppData/Roaming/Kodi"
destination_dir = "D:/_DEPLOYMENT/Pack"
directories_to_copy = ["addons", "media", "userdata"]

# Function to get the modification time of a file
def get_modification_time(file_path):
    return datetime.fromtimestamp(os.path.getmtime(file_path))

# Function to sync files from source to destination
def sync_files(source_dir, dest_dir):
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            source_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(source_file_path, source_dir)
            dest_file_path = os.path.join(dest_dir, relative_path)

            # Check if the file exists in destination
            if os.path.isfile(dest_file_path):
                # Compare modification times
                source_time = get_modification_time(source_file_path)
                dest_time = get_modification_time(dest_file_path)
                if source_time > dest_time:
                    print(f"Found newer file: {source_file_path} -> Replacing: {dest_file_path}")
                    shutil.copy2(source_file_path, dest_file_path)
                else:
                    print(f"No change: {source_file_path} is up to date.")
            else:
                print(f"New file: {source_file_path} -> Copying to: {dest_file_path}")
                os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
                shutil.copy2(source_file_path, dest_file_path)

# Function to copy directories from source to destination
def copy_directories():
    if not os.path.exists(destination_dir):
        print(f"Creating destination directory: {destination_dir}")
        os.makedirs(destination_dir)

    for dir_name in directories_to_copy:
        source_path = os.path.join(source_dir, dir_name)
        dest_path = os.path.join(destination_dir, dir_name)

        if os.path.isdir(source_path):
            if not os.path.isdir(dest_path):  # Check if the directory exists in the destination
                print(f"Copying {dir_name} from {source_path} to {dest_path}")
                shutil.copytree(source_path, dest_path)
            else:
                print(f"Directory {dir_name} already exists in destination. Checking for updated files...")
                # Sync files if directory already exists in destination
                sync_files(source_path, dest_path)
        else:
            print(f"Warning: Directory {source_path} does not exist. Skipping.")

# Function to zip the directories
def zip_directories():
    zip_name = os.path.join(destination_dir, "Sanctum_v0.7.zip")
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for dir_name in directories_to_copy:
            dir_path = os.path.join(destination_dir, dir_name)
            if os.path.isdir(dir_path):
                # Walk through the directory and add each file to the zip
                for root, dirs, files in os.walk(dir_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Add the file to the zip file, keeping the relative path structure
                        zipf.write(file_path, os.path.relpath(file_path, destination_dir))
                print(f"Directory {dir_name} added to zip.")
            else:
                print(f"Warning: Directory {dir_name} not found for zipping.")

# Run the functions
def main():
    print("Checking and copying directories if needed...")
    copy_directories()
    print("Zipping directories...")
    zip_directories()
    print("Process complete!")

if __name__ == "__main__":
    main()