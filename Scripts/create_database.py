import sqlite3
import os

# Database folder path
db_folder = r"C:\Users\Lenovo\Cricksheet_Project\database"
os.makedirs(db_folder, exist_ok=True)

# Database file path
db_path = os.path.join(db_folder, "cricsheet.db")

# SQLite database create karo
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Example table create
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

conn.commit()
conn.close()

print(f"Database created at: {db_path}")
