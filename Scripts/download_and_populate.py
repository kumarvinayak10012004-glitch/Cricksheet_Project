import os
import requests
import zipfile
import io
import json
import sqlite3

# Paths
json_folder = r"C:\Users\Lenovo\Cricksheet_Project\data\json"
db_path = r"C:\Users\Lenovo\Cricksheet_Project\database\cricsheet.db"

# Create folders if not exist
os.makedirs(json_folder, exist_ok=True)
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Cricsheet GitHub ZIP URLs
urls = {
    "ODI": "https://github.com/cricsheet/cricsheet-data/archive/refs/heads/master.zip"
    # Tum specific formats ke liye bhi alag URL add kar sakte ho
}

# Download and extract JSON files
for key, url in urls.items():
    print(f"Downloading {key} data...")
    r = requests.get(url)
    if r.status_code == 200:
        z = zipfile.ZipFile(io.BytesIO(r.content))
        for file in z.namelist():
            if file.endswith(".json"):
                # Extract to json_folder
                z.extract(file, json_folder)
        print(f"{key} JSON files downloaded and extracted.")
    else:
        print(f"Failed to download {key} data. Status code: {r.status_code}")

# Connect to SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create tables if not exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS matches (
    match_id TEXT PRIMARY KEY,
    date TEXT,
    team1 TEXT,
    team2 TEXT,
    venue TEXT,
    result TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS balls (
    ball_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id TEXT,
    inning INTEGER,
    over INTEGER,
    ball_number INTEGER,
    batsman TEXT,
    bowler TEXT,
    runs INTEGER,
    FOREIGN KEY(match_id) REFERENCES matches(match_id)
)
""")

# Insert function
def insert_match(match_id, info):
    cursor.execute("""
        INSERT OR IGNORE INTO matches (match_id, date, team1, team2, venue, result)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        match_id,
        info.get('date', ''),
        info.get('team1', ''),
        info.get('team2', ''),
        info.get('venue', ''),
        info.get('result', '')
    ))

def insert_balls(match_id, innings):
    for inning in innings:
        inning_number = inning.get('number', 1)
        for over in inning.get('overs', []):
            over_number = over.get('number', 0)
            for ball in over.get('deliveries', []):
                cursor.execute("""
                    INSERT INTO balls (match_id, inning, over, ball_number, batsman, bowler, runs)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    match_id,
                    inning_number,
                    over_number,
                    ball.get('number', 0),
                    ball.get('batsman', ''),
                    ball.get('bowler', ''),
                    ball.get('runs', 0)
                ))

# Populate database
json_files = [os.path.join(json_folder, f) for f in os.listdir(json_folder) if f.endswith(".json")]

if not json_files:
    print("No JSON files found in folder. Please check downloads.")
else:
    for file_path in json_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                match_id = data.get('info', {}).get('match_id', os.path.basename(file_path))
                match_info = {
                    'date': data.get('info', {}).get('dates', [''])[0],
                    'team1': data.get('info', {}).get('teams', ['',''])[0],
                    'team2': data.get('info', {}).get('teams', ['',''])[1],
                    'venue': data.get('info', {}).get('venue', ''),
                    'result': data.get('info', {}).get('outcome', {}).get('winner', '')
                }
                insert_match(match_id, match_info)
                insert_balls(match_id, data.get('innings', []))
            except Exception as e:
                print(f"Failed to process {file_path}: {e}")

    conn.commit()
    conn.close()
    print("All JSON data inserted into the database successfully!")
