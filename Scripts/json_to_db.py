import os
import json
import sqlite3

# Paths
db_path = r"C:\Users\Lenovo\Cricksheet_Project\database\cricsheet.db"
json_folder = r"C:\Users\Lenovo\Cricksheet_Project\data\json"

# Connect to SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Function to insert match data
def insert_match(match_id, match_info):
    cursor.execute("""
        INSERT OR IGNORE INTO matches (match_id, date, team1, team2, venue, result)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        match_id,
        match_info.get('date', ''),
        match_info.get('team1', ''),
        match_info.get('team2', ''),
        match_info.get('venue', ''),
        match_info.get('result', '')
    ))

# Function to insert ball-by-ball data
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

# Loop through all JSON files
for file_name in os.listdir(json_folder):
    if file_name.endswith('.json'):
        file_path = os.path.join(json_folder, file_name)
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        match_id = data.get('info', {}).get('match_id', file_name)  # unique id
        match_info = {
            'date': data.get('info', {}).get('dates', [''])[0],
            'team1': data.get('info', {}).get('teams', ['',''])[0],
            'team2': data.get('info', {}).get('teams', ['',''])[1],
            'venue': data.get('info', {}).get('venue', ''),
            'result': data.get('info', {}).get('outcome', {}).get('winner', '')
        }
        
        insert_match(match_id, match_info)
        insert_balls(match_id, data.get('innings', []))

# Commit and close
conn.commit()
conn.close()

print("All JSON data inserted into the database successfully!")
