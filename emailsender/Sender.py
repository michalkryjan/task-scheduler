import os
import smtplib, ssl
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.environ['EMAIL_ADDRESS']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']

context = ssl.create_default_context()

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    subject = 'Tasks for today (get name of day here and date)'
    body = 'Something'
    msg = f'Subject: {subject}\n\n{body}'

    server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)
except Exception as e:
    print(e)
finally:
    server.quit()
