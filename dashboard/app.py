# dashboard/app.py

import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(page_title="📊 Dashboard BOT", layout="wide")

st.title("📊 Dashboard BOT Cruce MA")

# Conexión a la base SQLite compartida
conn = sqlite3.connect("/app/db/bot_trades.db")

# Carga de operaciones
df = pd.read_sql_query("SELECT * FROM operaciones ORDER BY timestamp DESC", conn)

st.subheader("📋 Últimas operaciones")
st.dataframe(df.head(20), use_container_width=True)

# Profit acumulado
profit_total = df["profit"].sum()
st.metric("💰 Profit total acumulado", f"{profit_total:.2f} USDT")

# Gráfico simple
st.subheader("📈 Profit a lo largo del tiempo")
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp")
df["profit_cumsum"] = df["profit"].cumsum()
st.line_chart(df.set_index("timestamp")["profit_cumsum"])
