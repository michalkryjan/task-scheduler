from emailsender.createEmail import createFullEmail
import smtplib
import ssl
import os
import pathlib
from configparser import ConfigParser


def sendEmail(email):
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls(context=context)
        server.login(EMAIL_ADDRESS, APP_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, email.as_string())
    except Exception as e:
        print(e)
    finally:
        server.quit()


rootFolder = pathlib.PureWindowsPath(os.path.abspath(__file__)).parents[1]
configFilePath = os.path.join(rootFolder, 'config.ini')
config = ConfigParser()

config.read(configFilePath)
is_active = config.get('sender', 'is_active')
if is_active == 'yes':
    EMAIL_ADDRESS = config.get('sender', 'email')
    APP_PASSWORD = config.get('sender', 'password')
    email = createFullEmail(EMAIL_ADDRESS, EMAIL_ADDRESS)
    sendEmail(email)
