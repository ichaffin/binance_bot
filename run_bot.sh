#!/bin/bash
cd /home/dockeradmin/proyectos/binance_bot
/usr/bin/docker compose up --abort-on-container-exit >> /home/dockeradmin/cron_log.txt 2>&1

