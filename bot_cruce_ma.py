import os
import logging
from datetime import datetime
from utils import (
    get_client,
    get_data,
    detectar_senal,
    ejecutar_orden,
    guardar_operacion,
    enviar_alerta
)

# === LOGGER ===
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "bot.log")),
        logging.StreamHandler()
    ],
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("bot_logger")

client = get_client()

symbols = ["BTCUSDT", "ETHUSDT"]
short_window = 50
long_window = 200
usdt_amount = 8.0

def main():
    logger.info("=== BOT CRUCE MA - INICIANDO ===")

    # 📧 Mail de keep-alive
    enviar_alerta(
        "BOT CRUCE MA - Keep Alive",
        f"El bot está activo. Hora: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )

    for symbol in symbols:
        df = get_data(client, symbol, short_window, long_window)
        signal = detectar_senal(df)

        if signal:
            order = ejecutar_orden(client, symbol, signal, usdt_amount)
            if order:
                logger.info(f"{signal} ejecutada en {symbol}")

                qty = float(order['executedQty']) if 'executedQty' in order else 0
                price = float(order['fills'][0]['price'])

                guardar_operacion(symbol, signal, price, qty)

                # 📧 Mail de ejecución real
                enviar_alerta(
                    f"BOT CRUCE MA - {signal} ejecutada",
                    f"✅ Symbol: {symbol}\nTipo: {signal}\nPrecio: {price}\nCantidad: {qty}"
                )
            else:
                logger.warning(f"No se pudo ejecutar {signal} en {symbol}")
        else:
            logger.info(f"Sin señal para {symbol}")

    logger.info("=== BOT CRUCE MA - FINALIZADO ===")

if __name__ == "__main__":
    main()
