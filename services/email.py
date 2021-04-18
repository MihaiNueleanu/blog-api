from services.utils import fire_and_forget
import smtplib

from settings import settings


def get_client():
    client = smtplib.SMTP_SSL(host=settings.SMTP_SERVER,
                              port=settings.SMTP_PORT)
    client.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
    return client


@fire_and_forget
def send_email(receiver: str, text: str, subject="dotmethod"):
    client = get_client()
    sender = settings.SMTP_USER

    payload = "Subject: {}\n\n{}".format(subject, text)

    client.sendmail(sender, receiver, payload)
    print(f"Sent mail. Subject: {subject}")
