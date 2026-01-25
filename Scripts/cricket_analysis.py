import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

# ---------------------------
# 1. Connect to DB
# ---------------------------
DB_PATH = r"C:\Users\Lenovo\Cricksheet_Project\Scripts\cricsheet.db"
conn = sqlite3.connect(DB_PATH)

# ---------------------------
# 2. Inspect balls table columns
# ---------------------------
columns_df = pd.read_sql("PRAGMA table_info(balls);", conn)
columns = columns_df['name'].tolist()
print("Columns in balls table:", columns)

batsman_col = 'batsman' if 'batsman' in columns else columns[0]
bowler_col = 'bowler' if 'bowler' in columns else columns[0]
runs_col = 'runs' if 'runs' in columns else columns[0]
match_col = 'match_id' if 'match_id' in columns else columns[0]

# ---------------------------
# 3. Top 10 Run Scorers
# ---------------------------
query_top_batsmen = f"""
    SELECT {batsman_col} as batsman, SUM({runs_col}) as total_runs
    FROM balls
    GROUP BY {batsman_col}
    ORDER BY total_runs DESC
    LIMIT 10;
"""
top_batsmen = pd.read_sql(query_top_batsmen, conn)
print("\nTop 10 Batsmen:")
print(top_batsmen)

plt.figure(figsize=(10,6))
sns.barplot(x="total_runs", y="batsman", data=top_batsmen, palette="Blues_d")
plt.title("Top 10 Batsmen by Runs")
plt.xlabel("Total Runs")
plt.ylabel("Batsman")
plt.tight_layout()
plt.savefig("top_batsmen.png")
plt.show()

# ---------------------------
# 4. Top 10 Wicket Takers
# ---------------------------
if 'dismissal_kind' in columns:
    query_wickets = f"""
        SELECT {bowler_col} as bowler, COUNT(*) as wickets
        FROM balls
        WHERE dismissal_kind IS NOT NULL
        GROUP BY {bowler_col}
        ORDER BY wickets DESC
        LIMIT 10;
    """
    top_wickets = pd.read_sql(query_wickets, conn)
    print("\nTop 10 Wicket Takers:")
    print(top_wickets)

    plt.figure(figsize=(10,6))
    sns.barplot(x="wickets", y="bowler", data=top_wickets, palette="Reds_d")
    plt.title("Top 10 Wicket Takers")
    plt.xlabel("Total Wickets")
    plt.ylabel("Bowler")
    plt.tight_layout()
    plt.savefig("top_wickets.png")
    plt.show()

# ---------------------------
# 5. Match-wise Total Runs
# ---------------------------
query_match_runs = f"""
    SELECT {match_col} as match_id, SUM({runs_col}) as total_runs
    FROM balls
    GROUP BY {match_col}
    ORDER BY {match_col};
"""
match_runs = pd.read_sql(query_match_runs, conn)
print("\nMatch-wise Total Runs (first 10 matches):")
print(match_runs.head(10))

plt.figure(figsize=(12,6))
sns.lineplot(x="match_id", y="total_runs", data=match_runs, marker="o")
plt.title("Match-wise Total Runs")
plt.xlabel("Match ID")
plt.ylabel("Total Runs")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("match_runs.png")
plt.show()

# ---------------------------
# 6. Save CSVs
# ---------------------------
top_batsmen.to_csv("top_batsmen.csv", index=False)
match_runs.to_csv("match_runs.csv", index=False)
if 'dismissal_kind' in columns:
    top_wickets.to_csv("top_wickets.csv", index=False)

print("\nCSV files saved: top_batsmen.csv, match_runs.csv, top_wickets.csv (if available)")

# ---------------------------
# 7. Close DB
# ---------------------------
conn.close()








