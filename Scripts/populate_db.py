import sqlite3
import pandas as pd
import os

# Paths
DB_PATH = "cricsheet.db"
OUTPUT_PATH = "../output"

# Connect to SQLite DB
conn = sqlite3.connect(DB_PATH)

# Function to load CSV into DB
def load_csv_to_db(csv_file, table_name):
    csv_path = os.path.join(OUTPUT_PATH, csv_file)
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Table '{table_name}' created with {len(df)} rows.")
    else:
        print(f"CSV file '{csv_file}' not found in {OUTPUT_PATH}!")

# Load tables
load_csv_to_db("matches.csv", "matches")
load_csv_to_db("balls.csv", "balls")

# Close connection
conn.close()
print("Database population complete!")
