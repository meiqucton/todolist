import os
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()

mail = Mail()

def init_mail(app):
    app.config.update(
        MAIL_SERVER="smtp.gmail.com",
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
        MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
        MAIL_DEFAULT_SENDER=os.getenv('MAIL_DEFAULT_SENDER')
    )
    mail.init_app(app)

def send_email(subject, recipients, body, html ):
    msg = Message(subject=subject, recipients=recipients, body=body, html=html)
    mail.send(msg)
