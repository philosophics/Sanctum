import os

# Specify the original file name
original_file = "plugin.program.Sanctum.zip"

# Specify the version to append
version = "-0.07"

# Ensure the file exists
if os.path.isfile(original_file):
    # Split the file into name and extension
    name, ext = os.path.splitext(original_file)
    
    # Create the new file name
    new_file = f"{name}{version}{ext}"
    
    # Rename the file
    os.rename(original_file, new_file)
    print(f"Renamed: '{original_file}' to '{new_file}'")
else:
    print(f"File '{original_file}' not found in the current directory.")