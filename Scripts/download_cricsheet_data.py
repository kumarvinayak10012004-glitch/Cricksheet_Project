import requests
import zipfile
import os

# Base download URLs
zip_urls = {
    "Test": "https://cricsheet.org/downloads/tests_json.zip",
    "ODI": "https://cricsheet.org/downloads/odis_json.zip",
    "T20": "https://cricsheet.org/downloads/t20s_json.zip",
    "IPL": "https://cricsheet.org/downloads/ipl_json.zip"
}

base_dir = r"C:\Users\Lenovo\Cricksheet_Project"

for match_type, url in zip_urls.items():
    print(f"Downloading {match_type} data...")

    zip_path = os.path.join(base_dir, f"{match_type}.zip")

    # Download ZIP
    response = requests.get(url)
    with open(zip_path, "wb") as f:
        f.write(response.content)

    # Extract ZIP
    extract_path = os.path.join(base_dir, match_type)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    print(f"{match_type} data extracted to {extract_path}")

print("All downloads completed successfully!")
