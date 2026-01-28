import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

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


