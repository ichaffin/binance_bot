# utils.py
import os
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import logging
from binance.client import Client
from datetime import datetime

load_dotenv()

logger = logging.getLogger("bot_logger")

# === DB ===
conn = sqlite3.connect("db/bot_trades.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS operaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    tipo TEXT,
    precio REAL,
    cantidad REAL,
    profit REAL,
    timestamp TEXT
)
""")
conn.commit()

# === Binance ===
#def get_client():
#    return Client(os.getenv("BINANCE_API_KEY"), os.getenv("BINANCE_API_SECRET"))

def get_client():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    if not api_key or not api_secret:
        raise ValueError("❌ API_KEY o API_SECRET no están definidos")
    return Client(api_key, api_secret)

# === Get data ===
def get_data(client, symbol, short_window, long_window):
    df = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR, "200 hours ago UTC")
    import pandas as pd
    import numpy as np
    df = pd.DataFrame(df)
    df.columns = ["ts","open","high","low","close","volume","ct","qav","n","tbv","tqv","i"]
    df["date"] = pd.to_datetime(df["ts"], unit="ms")
    df["close"] = df["close"].astype(float)
    df["short_ma"] = df["close"].rolling(short_window).mean()
    df["long_ma"] = df["close"].rolling(long_window).mean()
    return df

def detectar_senal(df):
    if df.empty:
        return None
    last = df.iloc[-1]
    if last["short_ma"] > last["long_ma"] and df.iloc[-2]["short_ma"] <= df.iloc[-2]["long_ma"]:
        return "BUY"
    if last["short_ma"] < last["long_ma"] and df.iloc[-2]["short_ma"] >= df.iloc[-2]["long_ma"]:
        return "SELL"
    return None

def ejecutar_orden(client, symbol, signal, usdt_amount):
    from binance.enums import SIDE_BUY, SIDE_SELL, ORDER_TYPE_MARKET
    info = client.get_symbol_info(symbol)
    price = float(client.get_symbol_ticker(symbol=symbol)['price'])
    asset = symbol.replace("USDT", "")

    if signal == "BUY":
        return client.create_order(symbol=symbol, side=SIDE_BUY, type=ORDER_TYPE_MARKET, quoteOrderQty=usdt_amount)
    else:
        balance = float(client.get_asset_balance(asset=asset)['free'])
        qty = usdt_amount / price
        min_qty, step = 0, 0
        for f in info['filters']:
            if f['filterType'] == 'LOT_SIZE':
                min_qty = float(f['minQty'])
                step = float(f['stepSize'])
        qty = float(int(qty/step) * step)
        if qty < min_qty or qty > balance:
            return None
        return client.create_order(symbol=symbol, side=SIDE_SELL, type=ORDER_TYPE_MARKET, quantity=qty)

def guardar_operacion(symbol, tipo, precio, cantidad, profit=0.0):
    cursor.execute("""
    INSERT INTO operaciones (symbol, tipo, precio, cantidad, profit, timestamp)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (symbol, tipo, precio, cantidad, profit, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()

# === Mail ===
def enviar_alerta(subject, body):
    logger.info("Enviando correo...")
    remitente = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    destinatario = os.getenv("EMAIL_DEST")

    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    servidor = smtplib.SMTP('smtp.gmail.com', 587)
    servidor.starttls()
    servidor.login(remitente, password)
    servidor.send_message(msg)
    servidor.quit()
    logger.info(f"✅ Correo enviado correctamente a {destinatario}")
