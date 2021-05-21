from PyQt5.QtCore import Qt, QTime
from PyQt5.QtWidgets import QFormLayout, QLineEdit, QTimeEdit
from ..Defaults import *


class SettingsAdditionalMenuView(QFormLayout):
    def __init__(self):
        super().__init__()
        self.emailAddressInput = self.createEmailAddressInput()
        self.appPasswordInput = self.createAppPasswordInput()
        self.timeSetterInput = self.createTimeSetterInput()
        self.addRow(self.createEmailAddressLabel(), self.emailAddressInput)
        self.addRow(self.createAppPasswordLabel(), self.appPasswordInput)
        self.addRow(self.createTimeSetterLabel(), self.timeSetterInput)

    def createEmailAddressLabel(self):
        label = createDefaultOneLineLabel('Your email address: ')
        setDefaultFontForSettings(label)
        setMaxSizeForWidget(label, 150, 320)
        return label

    def createEmailAddressInput(self):
        email = QLineEdit()
        setDefaultFontForSettings(email)
        setMaxSizeForWidget(email, 150, 320)
        return email

    def createAppPasswordLabel(self):
        label = createDefaultOneLineLabel('Your app password: ')
        setDefaultFontForSettings(label)
        setMaxSizeForWidget(label, 150, 320)
        return label

    def createAppPasswordInput(self):
        password = QLineEdit()
        setDefaultFontForSettings(password)
        setMaxSizeForWidget(password, 150, 320)
        return password

    def createTimeSetterLabel(self):
        labelText = 'At what time do you want to get your\'s to-do list?'
        label = createDefaultOneLineLabel(labelText)
        setDefaultFontForSettings(label)
        setMaxSizeForWidget(label, 150, 320)
        return label

    def createTimeSetterInput(self):
        defaultTime = QTime(7, 0)
        timeSetter = QTimeEdit(defaultTime)
        setDefaultFontForSettings(timeSetter)
        setMaxSizeForWidget(timeSetter, 50, 100)
        return timeSetter
