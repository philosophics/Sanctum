import os
import shutil
from datetime import datetime

source_dir = r"D:/_DEPLOYMENT/Zips"  # Source directory where the zip files are located
destination_dir = r"D:/_DEPLOYMENT/Sanctum"  # Destination directory to scan and replace files

# We will ignore this folder within the source directory
ignore_folder = "Forked"

def get_modification_time(file_path):
    """Returns the last modification time of the given file."""
    return datetime.fromtimestamp(os.path.getmtime(file_path))

def sync_file(source_file, dest_file):
    """Syncs a single file by comparing modification times and copying if source is newer."""
    if os.path.isfile(source_file):
        if os.path.isfile(dest_file):
            source_time = get_modification_time(source_file)
            dest_time = get_modification_time(dest_file)
            if source_time > dest_time:
                print(f"Found newer file: {source_file} -> Replacing: {dest_file}")
                shutil.copy2(source_file, dest_file)
            elif source_time == dest_time:
                print(f"No change: {source_file} and {dest_file} have the same modification date.")
            else:
                print(f"Destination file is newer: {dest_file}. No replacement needed.")
        else:
            print(f"Found new file: {source_file} -> Copying to: {dest_file}")
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            shutil.copy2(source_file, dest_file)

def sync_zip_files():
    """Syncs all zip files from the source directory to the destination directory."""
    if not os.path.isdir(source_dir):
        print(f"Warning: Source directory does not exist: {source_dir}. Skipping zip file sync.")
        return

    # Walk through the source directory and its subdirectories
    for root, dirs, files in os.walk(source_dir):
        # Skip the Forked directory
        if os.path.basename(root) == ignore_folder:
            continue

        for file_name in files:
            if file_name.endswith(".zip"):
                source_file_path = os.path.join(root, file_name)

                # Now we check the destination directory and its subdirectories
                for subdir_root, subdir_dirs, subdir_files in os.walk(destination_dir):
                    if file_name in subdir_files:
                        dest_file_path = os.path.join(subdir_root, file_name)

                        # If a matching zip file is found, replace it
                        if os.path.isfile(source_file_path):
                            print(f"Processing zip file: {file_name}")
                            sync_file(source_file_path, dest_file_path)

def sync_files():
    """Main function to call the sync for zip files."""
    print("Checking and syncing zip files...")
    sync_zip_files()

    print("Sync complete!")

if __name__ == "__main__":
    sync_files()