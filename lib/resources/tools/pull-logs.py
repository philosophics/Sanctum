import os
import subprocess
import platform
import ipaddress
import shutil  # For copying files from Windows file system

def list_adb_devices():
    """Lists all devices connected via ADB."""
    try:
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True, check=True)
        devices = result.stdout.splitlines()[1:]  # Skip the first line ('List of devices attached')
        return [line.split()[0] for line in devices if "device" in line]
    except subprocess.CalledProcessError as e:
        print("Error running ADB:", e)
        return []

def connect_network_devices():
    """Scans both 192.168.1.x and 10.0.0.x IP ranges and attempts to connect to ADB devices."""
    found_devices = []
    # Define the IP ranges to scan
    ranges = [
        ipaddress.IPv4Network('192.168.1.0/255', strict=False),  # 192.168.1.1 - 192.168.1.255
        ipaddress.IPv4Network('10.0.0.0/255', strict=False),    # 10.0.0.1 - 10.0.0.255
    ]

    # Function to attempt connection to a given IP
    def try_connect(ip):
        try:
            result = subprocess.run(['adb', 'connect', f'{ip}:5555'], capture_output=True, text=True, timeout=2)
            if "connected" in result.stdout.lower() or "already connected" in result.stdout.lower():
                found_devices.append(ip)
                print(f"Connected to {ip}")
            else:
                print(f"Failed to connect to {ip}: {result.stderr}")
        except subprocess.TimeoutExpired:
            pass  # Skip on timeout

    # Scan both IP ranges
    for ip_range in ranges:
        for ip in ip_range.hosts():  # Iterate over each host in the range
            print(f"Attempting to connect to {ip}...")
            try_connect(str(ip))

    return found_devices

def get_product_name(device):
    """Fetches the product name from the build.prop file."""
    try:
        result = subprocess.run(["adb", "-s", device, "shell", "getprop", "ro.product.model"], capture_output=True, text=True, check=True)
        return result.stdout.strip()  # Remove any extra whitespace/newlines
    except subprocess.CalledProcessError as e:
        print(f"Failed to get product name from {device}: {e}")
        return device  # Fallback to device ID if product name is not found

def pull_logs_from_devices(devices):
    """Pulls the Kodi log from all listed ADB devices."""
    for device in devices:
        print(f"Pulling log from device: {device}")
        
        # Get the product name from the device
        product_name = get_product_name(device)
        
        # Define the remote log path and local log path with product name
        remote_log_path = "/storage/emulated/0/Android/data/org.xbmc.kodi/files/.kodi/temp/kodi.log"
        local_log_path = f"remote-{product_name}-kodi.log"
        
        try:
            # Pull the remote log file from the device
            subprocess.run(["adb", "-s", device, "pull", remote_log_path, local_log_path], check=True)
            print(f"Log pulled from {device} (Product: {product_name})")
        except subprocess.CalledProcessError as e:
            print(f"Failed to pull log from {device}: {e}")
        
        # Now pull the local log file from the Windows file system (instead of using ADB)
        if platform.system() == 'Windows':
            local_kodi_log_path = "C:/Users/philo/AppData/Roaming/Kodi/kodi.log"
            if os.path.exists(local_kodi_log_path):
                try:
                    shutil.copy(local_kodi_log_path, "kodi.log")  # Copy it to current working directory
                    print(f"Local log copied from {local_kodi_log_path} to kodi.log")
                except Exception as e:
                    print(f"Failed to copy local log: {e}")
            else:
                print(f"Local Kodi log not found at {local_kodi_log_path}")

def main():
    print("Scanning for ADB devices...")

    # List local devices connected via USB
    devices = list_adb_devices()

    # If no devices found via USB, attempt to discover network devices
    if not devices:
        print("No devices found via ADB. Attempting to discover network devices...")
        devices = connect_network_devices()

    # Proceed to pull logs from all found devices
    if devices:
        print(f"Found devices: {devices}")
        pull_logs_from_devices(devices)
    else:
        print("No devices found on the network.")

if __name__ == "__main__":
    main()