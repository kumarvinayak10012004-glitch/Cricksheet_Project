import json
import os
import pandas as pd

INPUT_DIR = r"C:\Users\Lenovo\Cricksheet_Project\Test"
OUTPUT_CSV = r"C:\Users\Lenovo\Cricksheet_Project\output\balls.csv"

rows = []

for file in os.listdir(INPUT_DIR):
    if not file.endswith(".json"):
        continue

    file_path = os.path.join(INPUT_DIR, file)

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    match_id = data.get("info", {}).get("match_type_number")

    for innings in data.get("innings", []):
        for over in innings.get("overs", []):
            over_number = over.get("over")

            for delivery in over.get("deliveries", []):
                ball = delivery.get("ball")
                runs = delivery.get("runs", {}).get("total", 0)

                rows.append([
                    match_id,
                    over_number,
                    ball,
                    delivery.get("batter"),
                    delivery.get("bowler"),
                    runs
                ])

df = pd.DataFrame(
    rows,
    columns=[
        "match_id",
        "over",
        "ball",
        "batsman",
        "bowler",
        "runs"
    ]
)

df.to_csv(OUTPUT_CSV, index=False)

print(f"✅ Ball-by-ball CSV created with {len(df)} rows")


