from PyQt5.QtCore import Qt, QTime
from PyQt5.QtWidgets import QFormLayout, QLineEdit, QTimeEdit
from ..Defaults import *


class SettingsAdditionalMenuView(QFormLayout):
    def __init__(self, **kwargs):
        super().__init__()
        self.emailAddressInput = self.createEmailAddressInput(kwargs.get('email', None))
        self.appPasswordInput = self.createAppPasswordInput(kwargs.get('password', None))
        self.timeSetterInput = self.createTimeSetterInput(kwargs.get('time', None))
        self.addRow(self.createEmailAddressLabel(), self.emailAddressInput)
        self.addRow(self.createAppPasswordLabel(), self.appPasswordInput)
        self.addRow(self.createTimeSetterLabel(), self.timeSetterInput)

    def createEmailAddressLabel(self):
        label = createDefaultOneLineLabel('Your email address: ')
        setDefaultFontForSettings(label)
        setMaxSizeForWidget(label, 150, 320)
        return label

    def createEmailAddressInput(self, email):
        if email is not None:
            input = QLineEdit(email)
        else:
            input = QLineEdit()
        setDefaultFontForSettings(input)
        setMaxSizeForWidget(input, 150, 320)
        return input

    def createAppPasswordLabel(self):
        label = createDefaultOneLineLabel('Your app password: ')
        setDefaultFontForSettings(label)
        setMaxSizeForWidget(label, 150, 320)
        return label

    def createAppPasswordInput(self, password):
        if password is not None:
            input = QLineEdit(password)
        else:
            input = QLineEdit()
        setDefaultFontForSettings(input)
        setMaxSizeForWidget(input, 150, 320)
        return input

    def createTimeSetterLabel(self):
        labelText = 'At what time do you want to get your\'s to-do list?'
        label = createDefaultOneLineLabel(labelText)
        setDefaultFontForSettings(label)
        setMaxSizeForWidget(label, 150, 320)
        return label

    def createTimeSetterInput(self, currentTime):
        if currentTime is not None:
            currentTime = currentTime.split(':')
            time = QTime(int(currentTime[0]), int(currentTime[1]))
        else:
            time = QTime(7, 0)
        timeSetter = QTimeEdit(time)
        setDefaultFontForSettings(timeSetter)
        setMaxSizeForWidget(timeSetter, 50, 100)
        return timeSetter
