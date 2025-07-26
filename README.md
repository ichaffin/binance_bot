📊 Bot Cruce MA — Documentación Operativa
Este bot automatiza compras y ventas en Binance usando Cruce de Medias Móviles (MA).
Corre dentro de un contenedor Docker programado con cron para ejecutarse cada hora y apagarse solo.
El streaming de logs es opcional y manual, no se queda corriendo por defecto.

⚙️ Cómo funciona
Cada hora:

cron ejecuta: docker-compose run --rm bot_cruce_ma

Se crea un contenedor temporal.

El bot revisa señales, ejecuta compra/venta, escribe logs y manda mail.

El contenedor se elimina solo (--rm).

bot_test/
 ├── bot_cruce_ma.py
 ├── utils.py
 ├── docker-compose.yml
 ├── Dockerfile
 ├── requirements.txt
 ├── .env
 ├── db/
 ├── logs/
 ├── setup_local_cron.sh
 ├── README.md ✅


🕒 Programar la ejecución automática
1️⃣ Lanza el script de setup:
    chmod +x setup_local_cron.sh
    ./setup_local_cron.sh

2️⃣ Esto crea un cron job:
    0 * * * * cd ~/Documents/bot_test && docker-compose run --rm bot_cruce_ma

3️⃣ Verificar:
crontab -l

🚦 Stream de logs manual
El bot NO deja logs en consola por defecto (solo los graba en /logs/bot.log).
Si querés ver output en vivo, lanzalo manual:

docker-compose run --rm bot_cruce_ma
O con up:

docker-compose up bot_cruce_ma
Cuando termines, se apaga solo.

🧹 Desactivar el bot
Para detener la ejecución automática, solo elimina la línea del cron:

crontab -e
Y borrá la línea que contenga:

docker-compose run --rm bot_cruce_ma
📨 Logs y mails
Las operaciones quedan guardadas en logs/bot.log y en la base de datos db/operaciones.db.
Cada ciclo envía un mail de actividad.
Si hay compra o venta real, envía un mail adicional como alerta.

🔑 Seguridad
Nunca subas .env a Git.
Guarda API_KEY y API_SECRET en .env y/o variables del host.
Haz backup regular de db/ y logs/.

✅ Estado actual
✔️ Bot probado y funcional en local.
✔️ Cron configurado para ejecutar sin supervisión.
✔️ Sin dependencias de servidores externos.
✔️ IP doméstica → Binance sin bloqueos.

🟢 Checklist final
 Claves API OK.

 .env protegido.
 Cron activo solo cuando lo uses.
 Logs revisados regularmente.
 Respaldos actualizados.

🚀 Listo. Bot automático. Control total. 0 USD de costo.