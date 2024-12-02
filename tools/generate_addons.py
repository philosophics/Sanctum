import os
import hashlib

root_path = os.path.abspath("C:/Sanctum")
addons_xml_path = os.path.join(root_path, "addons.xml")
addons_md5_path = os.path.join(root_path, "addons.xml.md5")

def generate_addons_xml():
    addons_xml = "<addons>\n"
    found_addons = False

    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            if filename == "addon.xml":
                found_addons = True
                addon_file = os.path.join(dirpath, filename)
                print(f"Found addon.xml: {addon_file}")
                with open(addon_file, "r", encoding="utf-8") as f:
                    addon_content = f.read().strip()
                    addon_content = addon_content.replace('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', '').strip()
                    addons_xml += f"{addon_content}\n"

    if not found_addons:
        print("No addon.xml files were found in the specified directory structure.")
        return

    addons_xml += "</addons>"

    os.makedirs(os.path.dirname(addons_xml_path), exist_ok=True)

    with open(addons_xml_path, "w", encoding="utf-8") as f:
        f.write(addons_xml)

    print(f"Generated {addons_xml_path}")

def generate_md5():
    try:
        with open(addons_xml_path, "r", encoding="utf-8") as f:
            addons_xml_content = f.read()

        md5_hash = hashlib.md5(addons_xml_content.encode("utf-8")).hexdigest()

        with open(addons_md5_path, "w", encoding="utf-8") as f:
            f.write(md5_hash)

        print(f"Generated MD5 checksum: {md5_hash}")
        print(f"MD5 file created at: {addons_md5_path}")
    except FileNotFoundError:
        print(f"Error: {addons_xml_path} not found. Please ensure addons.xml exists.")
    except Exception as e:
        print(f"An error occurred: {e}")

generate_addons_xml()
generate_md5()
