import os
import subprocess
import ipaddress
import socket
import time
import shutil
from concurrent.futures import ThreadPoolExecutor

# Constants
LOGS_DIR = "D:/_DEPLOYMENT/"
PING_TIMEOUT = 500  # in ms
MAX_THREADS = 20  # Number of threads for parallel execution

# Ensure the logs directory exists
os.makedirs(LOGS_DIR, exist_ok=True)

# Function to pull local log
def pull_local_log():
    local_log_path = "C:/Users/philo/AppData/Roaming/Kodi/kodi.log"
    destination = os.path.join(LOGS_DIR, "local-kodi.log")
    try:
        shutil.copy(local_log_path, destination)
        print(f"Local log copied to {destination}")
    except Exception as e:
        print(f"Failed to copy local log: {e}")

# Function to ping a device
def ping_device(ip):
    try:
        result = subprocess.run(["ping", "-n", "1", "-w", str(PING_TIMEOUT), str(ip)],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return ip if result.returncode == 0 else None
    except subprocess.SubprocessError:
        return None

# Function to check if ADB port (5555) is open
def is_adb_port_open(ip):
    try:
        with socket.create_connection((str(ip), 5555), timeout=1):
            return ip
    except socket.error:
        return None

# Discover reachable devices
def discover_android_devices():
    print("Discovering reachable devices...")
    # Find local subnet
    local_ip_output = subprocess.check_output("ipconfig", encoding="utf-8")
    subnet = None
    for line in local_ip_output.splitlines():
        if "IPv4" in line:
            subnet = line.split(":")[1].strip()
            break
    if not subnet:
        print("Could not determine local subnet.")
        return []

    network = ipaddress.IPv4Network(f"{subnet}/24", strict=False)
    all_hosts = list(network.hosts())

    # Parallel ping devices
    print("Pinging devices in parallel...")
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        reachable_devices = list(filter(None, executor.map(ping_device, all_hosts)))

    print(f"Reachable devices: {reachable_devices}")

    # Check for ADB port open
    print("Checking ADB port in parallel...")
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        android_devices = list(filter(None, executor.map(is_adb_port_open, reachable_devices)))

    print(f"Android devices with ADB port open: {android_devices}")
    return android_devices

# Restart ADB server
def restart_adb():
    try:
        print("Restarting ADB server...")
        subprocess.run(["adb", "kill-server"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["adb", "start-server"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(2)
        print("ADB server restarted.")
    except subprocess.SubprocessError as e:
        print(f"Error restarting ADB: {e}")

# Connect to a device via ADB
def connect_device(ip):
    adb_ip = f"{ip}:5555"
    print(f"Attempting to connect to {adb_ip}...")
    try:
        result = subprocess.run(["adb", "connect", adb_ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "connected" in result.stdout.lower():
            print(f"Successfully connected to {adb_ip}")
            return True
        else:
            print(f"Failed to connect to {adb_ip}: {result.stdout}")
            return False
    except subprocess.SubprocessError as e:
        print(f"Error connecting to {adb_ip}: {e}")
        return False

# Get device name from build.prop
def get_device_name(ip):
    try:
        result = subprocess.run(["adb", "-s", f"{ip}:5555", "shell", "getprop", "ro.product.model"],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip() or "unknown-device"
    except subprocess.SubprocessError:
        return "unknown-device"

# Pull log from remote device
def pull_log_from_device(ip):
    device_name = get_device_name(ip)
    destination = os.path.join(LOGS_DIR, f"{device_name}-kodi.log")
    try:
        subprocess.run(["adb", "-s", f"{ip}:5555", "pull",
                        "/storage/emulated/0/Android/data/org.xbmc.kodi/files/.kodi/temp/kodi.log", destination],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        print(f"Log successfully pulled from {ip} to {destination}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to pull log from {ip}: {e}")

# Main function
def main():
    print("Starting log retrieval process...")
    pull_local_log()  # Pull local log first

    restart_adb()  # Restart ADB server once

    android_devices = discover_android_devices()  # Discover devices
    if not android_devices:
        print("No Android devices found.")
        return

    for device in android_devices:
        if connect_device(device):
            pull_log_from_device(device)
        else:
            print(f"Skipping log pull for {device} due to connection failure.")

if __name__ == "__main__":
    main()