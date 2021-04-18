from dotenv import load_dotenv
import os
import ssl
import smtplib
from emailsender.DefaultEmail import DefaultEmail


load_dotenv()

EMAIL_ADDRESS = os.environ['EMAIL_ADDRESS']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']

context = ssl.create_default_context()
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls(context=context)
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    mail = DefaultEmail(EMAIL_ADDRESS, EMAIL_ADDRESS)
    email = mail.email
    server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, email.as_string())
except Exception as e:
    print(e)
finally:
    server.quit()
