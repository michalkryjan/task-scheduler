from PyQt5.QtCore import QObject, pyqtSignal, Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QFormLayout, QHBoxLayout, QLineEdit, QTextEdit, QDateEdit, QComboBox, \
    QPushButton, QKeySequenceEdit, QSpacerItem, QTimeEdit
from ..Fonts import *
from ..Defaults import *

class SettingsAdditionalMenuView(QFormLayout):
    def __init__(self):
        super().__init__()
        self.addRow(self.createEmailAddressLabel(), self.createEmailAddressField())
        self.addRow(self.createAppPasswordLabel(), self.createAppPasswordInput())
        self.addRow(self.createTimeSetterLabel(), self.createTimeSetterInput())

    def createEmailAddressLabel(self):
        label = createDefaultOneLineLabel('Your email address: ')
        return label

    def createEmailAddressInput(self):
        email = QLineEdit()
        setMaxSizeForWidget(email, 50, 150)
        return email

    def createAppPasswordLabel(self):
        label = createDefaultOneLineLabel('Your app password: ')
        return label

    def createAppPasswordInput(self):
        password = QLineEdit()
        setMaxSizeForWidget(password, 50, 150)
        return password

    def createTimeSetterLabel(self):
        labelText = 'At what time do you want to get your\'s to-do list?'
        label = createDefaultOneLineLabel(labelText)
        return label

    def createTimeSetterInput(self):
        timeSetter = QTimeEdit()
        return timeSetter
