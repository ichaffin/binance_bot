# setup_bot.py

import os
import json
import shutil

def main():
    print("=== BOT SETUP ===")

    # Crear carpeta logs/
    if not os.path.exists("logs"):
        os.makedirs("logs")
        print("✅ Carpeta 'logs/' creada.")
    else:
        print("✔️ 'logs/' ya existe.")

    # Crear carpeta db/
    if not os.path.exists("db"):
        os.makedirs("db")
        print("✅ Carpeta 'db/' creada.")
    else:
        print("✔️ 'db/' ya existe.")

    # Crear orders.json dentro de db/
    orders_path = os.path.join("db", "orders.json")
    if not os.path.exists(orders_path):
        with open(orders_path, "w") as f:
            json.dump([], f, indent=4)
        print("✅ Archivo 'orders.json' inicializado en 'db/'.")
    else:
        print("✔️ 'orders.json' ya existe en 'db/'.")

    # Copiar .env.example a .env si no existe
    if os.path.exists(".env.example") and not os.path.exists(".env"):
        shutil.copy(".env.example", ".env")
        print("✅ Archivo '.env' creado a partir de '.env.example'. Editá tus claves!")
    elif os.path.exists(".env"):
        print("✔️ '.env' ya existe.")
    else:
        print("⚠️ No se encontró '.env.example', crea tu .env manualmente.")

    print("=== SETUP COMPLETO ===")

if __name__ == "__main__":
    main()

