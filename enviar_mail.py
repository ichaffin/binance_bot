import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("bot_logger")  # Reusa el logger principal

def enviar_alerta(subject, body):
    logger.info("Enviando correo...")

    remitente = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    destinatario = os.getenv("EMAIL_DEST", remitente)

    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remitente, password)
        servidor.send_message(msg)
        servidor.quit()
        logger.info(f"✅ Correo enviado correctamente a {destinatario}")

    except Exception as e:
        logger.error(f"❌ Error enviando correo: {str(e)}")
