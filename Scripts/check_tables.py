import sqlite3

conn = sqlite3.connect("cricsheet.db")
cur = conn.cursor()

tables = ["matches", "balls"]

for table in tables:
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    count = cur.fetchone()[0]
    print(f"Total rows in {table} table:", count)

conn.close()


