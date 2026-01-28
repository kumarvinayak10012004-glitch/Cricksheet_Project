import pandas as pd
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MATCHES_CSV = os.path.join(BASE_DIR, "output", "matches.csv")
BALLS_CSV   = os.path.join(BASE_DIR, "output", "balls.csv")
DB_PATH     = os.path.join(os.path.dirname(__file__), "cricsheet.db")

print("Reading CSVs...")
print(MATCHES_CSV)
print(BALLS_CSV)

df_matches = pd.read_csv(MATCHES_CSV)
df_balls   = pd.read_csv(BALLS_CSV)

conn = sqlite3.connect(DB_PATH)

df_matches.to_sql("matches", conn, if_exists="replace", index=False)
df_balls.to_sql("balls", conn, if_exists="replace", index=False)

conn.close()

print("✅ Database populated successfully")
print("Matches:", len(df_matches))
print("Balls:", len(df_balls))
