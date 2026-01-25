import os
import requests
import zipfile
import io
import json
import sqlite3
import pandas as pd

# Paths
json_folder = r"C:\Users\Lenovo\Cricksheet_Project\data\json"
db_path = r"C:\Users\Lenovo\Cricksheet_Project\database\cricsheet.db"

# Create folders if not exist
os.makedirs(json_folder, exist_ok=True)
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Cricsheet GitHub ZIP URLs (example: ODI + IPL)
urls = {
    "ODI": "https://github.com/cricsheet/cricsheet-data/archive/refs/heads/master.zip"
    # Add more if needed
}

# Download and extract JSON files
for key, url in urls.items():
    print(f"Downloading {key} data...")
    r = requests.get(url)
    if r.status_code == 200:
        z = zipfile.ZipFile(io.BytesIO(r.content))
        for file in z.namelist():
            if file.endswith(".json"):
                # Extract only JSON files
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

# Insert functions
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
json_files = []
for root, dirs, files in os.walk(json_folder):
    for f in files:
        if f.endswith(".json"):
            json_files.append(os.path.join(root, f))

if not json_files:
    print("No JSON files found. Please check downloads.")
else:
    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
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
    print("All JSON data inserted into the database successfully!")

# -------------------------
# Analysis Queries
# -------------------------
print("\n📊 Cricket Analysis Report\n")

# 1. Top 10 Batsmen
query_batsmen = """
SELECT batsman, SUM(runs) AS total_runs
FROM balls
GROUP BY batsman
ORDER BY total_runs DESC
LIMIT 10;
"""
top_batsmen = pd.read_sql_query(query_batsmen, conn)
print("🔥 Top 10 Batsmen (by runs):")
print(top_batsmen, "\n")

# 2. Top 10 Bowlers
query_bowlers = """
SELECT bowler, COUNT(*) AS wickets
FROM balls
WHERE runs = 0 AND bowler IS NOT NULL
GROUP BY bowler
ORDER BY wickets DESC
LIMIT 10;
"""
top_bowlers = pd.read_sql_query(query_bowlers, conn)
print("🔥 Top 10 Bowlers (by wickets):")
print(top_bowlers, "\n")

# 3. Highest Score in a Single Match
query_highest_scores = """
SELECT match_id, batsman, SUM(runs) AS score
FROM balls
GROUP BY match_id, batsman
ORDER BY score DESC
LIMIT 10;
"""
highest_scores = pd.read_sql_query(query_highest_scores, conn)
print("🔥 Highest Scores in a Single Match:")
print(highest_scores, "\n")

# 4. Total Matches Played by Each Team
query_matches = """
SELECT team AS Team, SUM(matches_played) AS Total_Matches FROM (
    SELECT team1 AS team, COUNT(*) AS matches_played FROM matches GROUP BY team1
    UNION ALL
    SELECT team2 AS team, COUNT(*) AS matches_played FROM matches GROUP BY team2
)
GROUP BY team
ORDER BY Total_Matches DESC;
"""
matches_played = pd.read_sql_query(query_matches, conn)
print("🔥 Total Matches Played by Each Team:")
print(matches_played, "\n")

# 5. Most Active Venues
query_venues = """
SELECT venue, COUNT(*) AS matches_count
FROM matches
GROUP BY venue
ORDER BY matches_count DESC
LIMIT 10;
"""
active_venues = pd.read_sql_query(query_venues, conn)
print("🔥 Most Active Venues:")
print(active_venues, "\n")

conn.close()
