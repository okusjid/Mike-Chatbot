from fastapi_mail import ConnectionConfig
from config.main import settings

conf = ConnectionConfig(
   MAIL_USERNAME=settings.MAIL_USERNAME,
   MAIL_PASSWORD=settings.MAIL_PASSWORD,
   MAIL_PORT=settings.MAIL_PORT,
   MAIL_SERVER=settings.MAIL_SERVER,
   MAIL_FROM=settings.MAIL_EMAIL,
   MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
   MAIL_STARTTLS = True,
   MAIL_SSL_TLS = False,
   USE_CREDENTIALS = True,
   VALIDATE_CERTS = True
)