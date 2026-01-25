import sqlite3
import pandas as pd
import os

BASE_DIR = r"C:\Users\Lenovo\Cricksheet_Project"
DB_PATH = os.path.join(BASE_DIR, "database", "cricsheet.db")

MATCHES_CSV = "C:\\Users\\Lenovo\\Cricksheet_Project\\output\\matches.csv"
BALL_CSV = "C:\\Users\\Lenovo\\Cricksheet_Project\\output\\balls.csv"

conn = sqlite3.connect(DB_PATH)

df_matches = pd.read_csv(MATCHES_CSV)
df_ball = pd.read_csv(BALL_CSV)

df_matches.to_sql("matches", conn, if_exists="replace", index=False)
df_ball.to_sql("ball_by_ball", conn, if_exists="replace", index=False)

conn.close()

print("✅ SQLite database created with matches & ball_by_ball tables")
