import os

source_dir = "D:/_DEPLOYMENT/Zips/"
original_file = os.path.join(source_dir, "plugin.program.Sanctum.zip")

# Specify the version to append
version = "-0.07"

# Construct the new file name with version
name, ext = os.path.splitext(original_file)
new_file = f"{name}{version}{ext}"

# Check if the new file already exists and delete it if it does
if os.path.isfile(new_file):
    print(f"File with version '{version}' already exists: {new_file}. Deleting it.")
    os.remove(new_file)

# Ensure the original file exists
if os.path.isfile(original_file):
    # Rename the original file
    os.rename(original_file, new_file)
    print(f"Renamed: '{original_file}' to '{new_file}'")
else:
    print(f"File '{original_file}' not found in the current directory.")