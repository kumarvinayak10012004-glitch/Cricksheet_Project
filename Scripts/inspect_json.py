import json
import os

# Change this to ONE actual file name from your Test / ODI / T20 folder
file_path = r"C:\Users\Lenovo\OneDrive\Desktop\cricket match analysis\odis_json"  # example

with open(file_path, "r", encoding="utf-8") as f:
    match = json.load(f)

print("Top-level keys in JSON:")
print(match.keys())
