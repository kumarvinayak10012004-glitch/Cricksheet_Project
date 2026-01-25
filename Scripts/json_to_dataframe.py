import json
import os
import pandas as pd

DATA_DIR = r"C:\Users\Lenovo\Cricksheet_Project\Test"

match_records = []

files = os.listdir(DATA_DIR)

for file in files[:10]:  # first 10 files for testing
    if file.endswith(".json"):
        file_path = os.path.join(DATA_DIR, file)

        with open(file_path, "r", encoding="utf-8") as f:
            match = json.load(f)

        info = match.get("info", {})

        record = {
            "match_id": file.replace(".json", ""),
            "match_type": info.get("match_type"),
            "date": info.get("dates", [None])[0],
            "venue": info.get("venue"),
            "team1": info.get("teams", [None, None])[0],
            "team2": info.get("teams", [None, None])[1],
            "winner": info.get("outcome", {}).get("winner"),
            "result": info.get("outcome", {}).get("result")
        }

        match_records.append(record)

df_matches = pd.DataFrame(match_records)

print(df_matches.head())
print("\nColumns:")
print(df_matches.columns)

OUTPUT_PATH = rOUTPUT_PATH = r"C:\Users\Lenovo\Cricksheet_Project\Output\matches.csv"
df_matches.to_csv(OUTPUT_PATH, index=False)

print(f"\nSaved to {OUTPUT_PATH}")
