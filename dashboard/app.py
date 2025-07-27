# dashboard/app.py

import sqlite3
import pandas as pd
import streamlit as st
import os

st.set_page_config(page_title="📊 Dashboard BOT", layout="wide")
st.title("📊 Dashboard BOT Cruce MA")

# === Ruta dinámica a la base de datos ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if os.path.exists("/app/db/bot_trades.db"):
    db_path = "/app/db/bot_trades.db"  # Ruta usada dentro del contenedor Docker
else:
    db_path = os.path.join(BASE_DIR, "..", "db", "bot_trades.db")  # Ruta local desde VSCode o WSL

# Conexión a la base SQLite
conn = sqlite3.connect(db_path)

# Carga de operaciones
df = pd.read_sql_query("SELECT * FROM operaciones ORDER BY timestamp DESC", conn)

# === Dashboard ===
st.subheader("📋 Últimas operaciones")
st.dataframe(df.head(20), use_container_width=True)

# Profit acumulado
profit_total = df["profit"].sum()
st.metric("💰 Profit total acumulado", f"{profit_total:.2f} USDT")

# Gráfico de profit acumulado
st.subheader("📈 Profit a lo largo del tiempo")
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp")
df["profit_cumsum"] = df["profit"].cumsum()
st.line_chart(df.set_index("timestamp")["profit_cumsum"])
