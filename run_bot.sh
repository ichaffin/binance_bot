#!/bin/bash

# Archivo: /home/dockeradmin/proyectos/binance_bot/run_bot.sh
# Descripción: Ejecuta el bot Binance dentro del contenedor Docker
# Fecha de última modificación: 2025-07-26

# Ruta al log
LOG_FILE="/home/dockeradmin/cron_log.txt"

# Agrega timestamp al log
echo "----- [$(date '+%Y-%m-%d %H:%M:%S')] Iniciando ejecución del bot -----" >> "$LOG_FILE"

# Cambiar al directorio del proyecto
cd /home/dockeradmin/proyectos/binance_bot || {
    echo "[ERROR] No se pudo acceder al directorio del bot" >> "$LOG_FILE"
    exit 1
}

# Ejecutar docker compose
/usr/bin/docker compose up --abort-on-container-exit >> "$LOG_FILE" 2>&1

# Registrar finalización
echo "----- [$(date '+%Y-%m-%d %H:%M:%S')] Ejecución finalizada -----" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

