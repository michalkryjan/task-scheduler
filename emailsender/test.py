import sys
sys.path.append('../')
from database.GetTasks import getForTodayTasks

tasks = getForTodayTasks()
content = '''Hey there! 

Here are your tasks for today:

'''
for task in tasks:
    content += f'{task.name}\n'
content += '\nHave a good day! ;)'

print(content)