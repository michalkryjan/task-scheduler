from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from emailsender.createHtmlEmail import createHtmlEmail
from database.GetTasks import getForTodayTasks

class DefaultEmail():
    def __init__(self, emailFrom, emailTo):
        super().__init__()
        self.email = MIMEMultipart('alternative')
        self.tasks = getForTodayTasks()
        self.email['Subject'] = self.createSubject()
        self.email['From'] = emailFrom
        self.email['To'] = emailTo
        createHtmlEmail()
        htmlEmail = open('CurrentEmail.html', 'r')
        htmlContent = MIMEText(htmlEmail.read(), 'html')
        plainContent = MIMEText(self.createPlainContent(), 'plain')
        self.email.attach(plainContent)
        self.email.attach(htmlContent)

    def createSubject(self):
        now = datetime.now()
        dayName = now.strftime('%A')
        date = now.strftime('%d.%m.%Y')
        subject = f'Your to-do list for {dayName} - {date}'
        return subject

    def createPlainContent(self):
        content = 'Hi there! \n\nHere are your tasks for today:\n\n'
        for task in self.tasks:
            content += f'{task.name}\n'
        content += '\nThat`s all. Good luck and have a nice day! ;)'
        return content
