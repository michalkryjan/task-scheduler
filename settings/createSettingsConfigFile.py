import os.path


def createSettingsConfigFile(shortcutKeysActive, shortcutKeys, senderActive):
    email = f'EMAIL_ADDRESS={email}\n'
    password = f'APP_PASSWORD={password}'
    file_dir = createPathToFile()
    with open(file_dir, 'w+') as file:
        file.write(email)
        file.write(password)


def createPathToFile():
    settings_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(settings_dir, "config.txt")
    return file_path
