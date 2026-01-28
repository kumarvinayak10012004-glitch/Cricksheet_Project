import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Cricsheet Cricket Analytics",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 Cricsheet Cricket Analytics Dashboard")

# -----------------------------
# Database connection
# -----------------------------
DB_PATH = "Scripts/cricsheet.db"

@st.cache_data
def load_data(query):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Options")
show_top_batsmen = st.sidebar.checkbox("Show Top Batsmen", value=True)

# -----------------------------
# Top Batsmen Section
# -----------------------------
if show_top_batsmen:
    st.subheader("🔥 Top 10 Batsmen by Total Runs")

    query = """
    SELECT batsman, SUM(runs) AS total_runs
    FROM balls
    GROUP BY batsman
    ORDER BY total_runs DESC
    LIMIT 10;
    """

    df = load_data(query)

    if df.empty:
        st.warning("No data found in database.")
    else:
        st.dataframe(df)

       # Plot
fig, ax = plt.subplots()  # <-- parentheses important!
ax.barh(df["batsman"], df["total_runs"])
ax.set_xlabel("Total Runs")
ax.set_ylabel("Batsman")
ax.set_title("Top 10 Batsmen")
ax.invert_yaxis()

st.pyplot(fig)


