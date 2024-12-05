import os
import shutil
import subprocess

# Directories and file paths
local_log_path = "C:/Users/philo/AppData/Roaming/Kodi/kodi.log"
destination_dir = "D:/_DEPLOYMENT"
destination_local_log = os.path.join(destination_dir, "kodi.log")
remote_log_path = "/sdcard/Android/data/org.xbmc.kodi/files/.kodi/temp/kodi.log"

# Ensure the destination directory exists
os.makedirs(destination_dir, exist_ok=True)

# Copy the local Kodi log
if os.path.isfile(local_log_path):
    shutil.copy2(local_log_path, destination_local_log)
    print(f"Copied: '{local_log_path}' to '{destination_local_log}'")
else:
    print(f"Local log file not found at: {local_log_path}")

# Check for adb and connected devices
try:
    result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")
    devices = [line.split("\t")[0] for line in lines[1:] if "device" in line]

    if devices:
        print(f"Found devices: {devices}")
        for device in devices:
            print(f"Attempting to pull log from device: {device}")
            destination_remote_log = os.path.join(destination_dir, f"{device}-kodi.log")
            pull_result = subprocess.run(
                ["adb", "-s", device, "pull", remote_log_path, destination_remote_log],
                capture_output=True,
                text=True
            )
            if "100%" in pull_result.stdout or os.path.isfile(destination_remote_log):
                print(f"Remote log copied to: {destination_remote_log}")
            else:
                print(f"Failed to pull the remote log from {device}. Output:\n{pull_result.stdout}")
    else:
        print("No devices found. Ensure devices are connected and USB debugging is enabled.")
except FileNotFoundError:
    print("ADB is not installed or not found in PATH. Please install ADB and try again.")

print("Log copy operation complete!")