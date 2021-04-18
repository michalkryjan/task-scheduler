import os
from shutil import copyfile
from database.GetTasks import getForTodayTasks
import pathlib


def createHtmlEmail():
    current_dir = pathlib.Path().absolute()
    source = os.path.abspath('top_template.html')
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

        with open('bottom_template.html', 'r') as file:
            for line in file:
                line = line.strip()
                mainFile.write(line)
