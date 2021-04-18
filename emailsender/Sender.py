from emailsender.createEmail import createFullEmail
from dotenv import load_dotenv
import smtplib
import ssl
import os


def sendEmail(email):
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls(context=context)
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, email.as_string())
    except Exception as e:
        print(e)
    finally:
        server.quit()


load_dotenv()
EMAIL_ADDRESS = os.environ['EMAIL_ADDRESS']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']

email = createFullEmail(EMAIL_ADDRESS, EMAIL_ADDRESS)
sendEmail(email)
