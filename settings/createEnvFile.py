import os.path


def createEnvFile(email, password):
    email = f'EMAIL_ADDRESS={email}\n'
    password = f'APP_PASSWORD={password}'
    file_dir = createPathToFile()
    with open(file_dir, 'w+') as file:
        file.write(email)
        file.write(password)


def createPathToFile():
    settings_dir = os.path.dirname(os.path.abspath(__file__))
    taskscheduler_dir = os.path.dirname(settings_dir)
    file_path = os.path.join(taskscheduler_dir, "emailsender", ".env")
    return file_path
