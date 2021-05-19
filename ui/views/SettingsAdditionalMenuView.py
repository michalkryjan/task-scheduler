from PyQt5.QtWidgets import QFormLayout, QLineEdit, QTimeEdit
from ..Defaults import *


class SettingsAdditionalMenuView(QFormLayout):
    def __init__(self):
        super().__init__()
        self.addRow(self.createEmailAddressLabel(), self.createEmailAddressInput())
        self.addRow(self.createAppPasswordLabel(), self.createAppPasswordInput())
        self.addRow(self.createTimeSetterLabel(), self.createTimeSetterInput())

    def createEmailAddressLabel(self):
        label = createDefaultOneLineLabel('Your email address: ')
        setDefaultFontForSettings(label)
        setMaxSizeForWidget(label, 100, 320)
        return label

    def createEmailAddressInput(self):
        email = QLineEdit()
        setDefaultFontForSettings(email)
        setMaxSizeForWidget(email, 100, 320)
        return email

    def createAppPasswordLabel(self):
        label = createDefaultOneLineLabel('Your app password: ')
        setDefaultFontForSettings(label)
        setMaxSizeForWidget(label, 100, 320)
        return label

    def createAppPasswordInput(self):
        password = QLineEdit()
        setDefaultFontForSettings(password)
        setMaxSizeForWidget(password, 100, 320)
        return password

    def createTimeSetterLabel(self):
        labelText = 'At what time do you want to get your\'s to-do list?'
        label = createDefaultOneLineLabel(labelText)
        setDefaultFontForSettings(label)
        setMaxSizeForWidget(label, 100, 320)
        return label

    def createTimeSetterInput(self):
        timeSetter = QTimeEdit()
        setDefaultFontForSettings(timeSetter)
        setMaxSizeForWidget(timeSetter, 50, 100)
        return timeSetter
