#!/bin/bash

echo "🚀 Configurando cron para bot_cruce_ma..."

PROJECT_PATH="$HOME/Documents/bot_test"

# Pone PATH explícito para cron
CRON_LINE="*/5 * * * * PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin && cd $PROJECT_PATH && docker-compose run --rm bot_cruce_ma >> $PROJECT_PATH/logs/cron_stdout.log 2>&1"

(crontab -l ; echo "$CRON_LINE") | sort - | uniq | crontab -

echo "✅ Cron job agregado:"
crontab -l
