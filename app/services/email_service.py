import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
from app.core.config import settings
import logging
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)


class EmailService:

    @staticmethod
    def send_email(subject: str, recipients: List[str], template_name: str, template_body: dict):

        try:

            template_dir = Path(__file__).parent.parent / 'templates' / 'email'
            env = Environment(loader=FileSystemLoader(template_dir))
            template = env.get_template(template_name)
            html_content = template.render(template_body)


            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = settings.MAIL_FROM
            message["To"] = ", ".join(recipients)
            part = MIMEText(html_content, "html")
            message.attach(part)


            context = ssl.create_default_context()
            with smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT) as server:
                server.starttls(context=context)
                server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
                server.sendmail(settings.MAIL_FROM, recipients, message.as_string())

            print(f"✅ Email successfully sent to: {recipients}")
            logger.info(f"Email successfully sent to: {recipients}")

        except Exception as e:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(f"❌ AN ERROR OCCURRED WHILE SENDING EMAIL: {e}")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            logger.error(f"Failed to send email to: {recipients}. Error: {e}")

            raise e
