from configparser import ConfigParser
import os


class Config(ConfigParser):
    def __init__(self, shortcutSettings, senderSettings):
        super().__init__()
        if os.path.exists('config.ini'):
            os.remove('config.ini')
        self.read('config.ini')
        self.shortcutSettings = shortcutSettings
        self.senderSettings = senderSettings
        self.add_section('shortcut_keys')
        self.add_section('sender')
        self.fillShortcutSection()
        self.fillSenderSection()

    def fillShortcutSection(self):
        if self.shortcutSettings is not None:
            self.set('shortcut_keys', 'is_active', 'yes')
            for i in range(1, len(self.shortcutSettings)+1):
                self.set('shortcut_keys', f'shortcut_key_{i}', self.shortcutSettings[i-1])
        else:
            self.set('shortcut_keys', 'is_active', 'no')

    def fillSenderSection(self):
        if self.senderSettings is not None:
            self.set('sender', 'is_active', 'yes')
            for key in self.senderSettings:
                self.set('sender', key, self.senderSettings[key])
        else:
            self.set('sender', 'is_active', 'no')

    def saveToIniFile(self):
        with open('config.ini', 'w') as file:
            self.write(file)
