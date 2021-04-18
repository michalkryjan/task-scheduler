from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from database.GetTasks import getForTodayTasks
from datetime import datetime
from shutil import copyfile
import os


def createFullEmail(emailFrom, emailTo):
    email = MIMEMultipart('alternative')
    email['Subject'] = createSubject()
    email['From'] = emailFrom
    email['To'] = emailTo
    createContentsForEmail(email)
    os.remove('CurrentEmail.html')
    return email


def createSubject():
    now = datetime.now()
    dayName = now.strftime('%A')
    date = now.strftime('%d.%m.%Y')
    subject = f'Your to-do list for {dayName} - {date}'
    return subject


def createContentsForEmail(email):
    createHtmlFileWithEmail()
    htmlEmail = open('CurrentEmail.html', 'r')
    htmlContent = MIMEText(htmlEmail.read(), 'html')
    plainContent = MIMEText(createPlainContent(), 'plain')
    email.attach(plainContent)
    email.attach(htmlContent)


def createPlainContent():
    tasks = getForTodayTasks()
    content = 'Hi there! \n\nHere are your tasks for today:\n\n'
    for task in tasks:
        content += f'{task.name}\n'
    content += '\nThat`s all. Good luck and have a nice day! ;)'
    return content


def createHtmlFileWithEmail():
    source = os.path.abspath('templates/top_template.html')
    copyfile(source, 'CurrentEmail.html')
    tasks = getForTodayTasks()
    with open('CurrentEmail.html', 'a') as mainFile:
        for task in tasks:
            taskHtml = f'''
<div style="padding: 20px; border: 1px solid black; border-radius: 10px; margin: 15px 0; width: 85%">
    <div style="height: auto; font-size: 15px; font-weight: bold; color: #181818;">
        <p>{task.name}</p>
    </div>
    <div style="height:auto; font-size: 12px; color: #686868">
        <p>{task.description}</p>
    </div>
</div>
            '''
            mainFile.write(taskHtml)
        with open('templates/bottom_template.html', 'r') as file:
            for line in file:
                line = line.strip()
                mainFile.write(line)
