from email.message import EmailMessage
from datetime import datetime
import sys
sys.path.append('../')
from database.GetTasks import getForTodayTasks


class DefaultEmail(EmailMessage):
    def __init__(self):
        super().__init__()
        self['Subject'] = self.createSubject()
        plainContent = self.createPlainContent()
        # htmlContent = self.createHtmlContent()
        self.set_content(plainContent)
        # self.add_alternative(htmlContent)

    def createSubject(self):
        now = datetime.now()
        dayName = now.strftime('%A')
        date = now.strftime('%d.%m.%Y')
        subject = f'Your tasks for {dayName} - {date}'
        return subject

    def createPlainContent(self):
        tasks = getForTodayTasks()
        content = '''Hey there! 

        Here are your tasks for today:

        '''
        for task in tasks:
            content += f'{task.name}\n'
        content += '\nHave a good day! ;)'
        return content

    def createHtmlContent(self):
        pass

    def setFromTo(self, emailFrom, emailTo):
        self['From'] = emailFrom
        self['To'] = emailTo
