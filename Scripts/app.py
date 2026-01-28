import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(page_title="Cricket Dashboard", layout="wide")

# -----------------------------
# Database path (Cloud-friendly)
# -----------------------------
DB_PATH = "Scripts/cricsheet.db"

# -----------------------------
# Function to load data from DB
# -----------------------------
@st.cache_data
def load_data(query):
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# -----------------------------
# Sidebar options
# -----------------------------
st.sidebar.title("Cricket Dashboard")
show_top_batsmen = st.sidebar.checkbox("Show Top Batsmen", True)

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
        st.warning("No data found in database.")  # <-- fixed closing quote
    else:
        # Show dataframe
        st.dataframe(df)

        # Plot horizontal bar chart using Plotly
        fig = px.bar(
            df,
            x="total_runs",
            y="batsman",
            orientation='h',
            title="Top 10 Batsmen",
            labels={"total_runs": "Total Runs", "batsman": "Batsman"}
        )
        fig.update_layout(yaxis=dict(autorange="reversed"))  # largest on top
        st.plotly_chart(fig, use_container_width=True)



