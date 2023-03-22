
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from settings import settings


def send_email(receiver: str, text: str, subject="dotmethod"):
    message = Mail(
        from_email=settings.MY_EMAIL,
        to_emails=receiver,
        subject=subject,
        plain_text_content=text,
    )

    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        sg.send(message)
        print(f"""Email sent to {receiver} with subject {subject}""")
    except Exception as e:
        print(
            f"""Email error while sending message to {receiver} with subject {subject}""", e)
