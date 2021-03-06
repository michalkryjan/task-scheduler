from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QHBoxLayout, QPushButton, QKeySequenceEdit, QSpacerItem
from ..Defaults import *
from .SettingsAdditionalMenuView import SettingsAdditionalMenuView
from .SettingsRequirementsDialog import RequirementsDialog
from settings.Config import Config
from configparser import ConfigParser
import pathlib
import os


class SettingsSignals(QObject):
    showMenu = pyqtSignal()
    hideMenu = pyqtSignal()
    saveSettings = pyqtSignal()


class SettingsMainView(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.signals = SettingsSignals()
        self.additionalMenu = QFormLayout()
        self.additionalLayout = QVBoxLayout()
        self.addLayout(self.createMainLayout())
        self.addLayout(self.additionalLayout)
        self.addLayout(self.createSaveButton())
        self.signals.showMenu.connect(self.showAdditionalMenu)
        self.signals.hideMenu.connect(self.hideAdditionalMenu)
        self.signals.saveSettings.connect(self.saveAllSettings)
        self.checkIfSenderIsActive()

    def createMainLayout(self):
        self.shortcutInput = self.createShortcutField()
        mainLayout = QFormLayout()
        mainLayout.addRow(self.createShortcutLabel(), self.shortcutInput)
        mainLayout.addItem(QSpacerItem(0, 20))
        mainLayout.addRow(self.createSenderToggleLabel(), self.createSenderToggle())
        return mainLayout

    def createShortcutLabel(self):
        labelText = 'Set shortcut keys for opening the app with the view of adding a new task at any moment:'
        label = createDefaultMultiLineLabel(labelText)
        label.setMaximumHeight(120)
        label.setMaximumWidth(700)
        setDefaultFontForSettings(label)
        return label

    def createShortcutField(self):
        currentConfig = self.getCurrentConfig()
        if currentConfig.get('shortcut_keys', 'is_active') == 'yes':
            currentShortcuts = self.convertShortcutsToString(currentConfig)
            field = QKeySequenceEdit(currentShortcuts)
        else:
            field = QKeySequenceEdit()
        field.setContentsMargins(10, 5, 0, 0)
        setMaxSizeForWidget(field, 70, 400)
        setDefaultFontForSettings(field)
        return field

    def getCurrentConfig(self):
        rootPath = pathlib.PureWindowsPath(os.path.abspath(__file__)).parents[2]
        config = ConfigParser()
        config.read(os.path.join(rootPath, 'config.ini'))
        return config

    def convertShortcutsToString(self, currentConfig):
        shortcutsString = ''
        i = 1
        while currentConfig.has_option('shortcut_keys', f'shortcut_key_{i}'):
            shortcutsString += currentConfig.get('shortcut_keys', f'shortcut_key_{i}') + ','
            i += 1
        return shortcutsString[:-1]

    def createSenderToggleLabel(self):
        labelText = 'Enable email sender feature? \n(you need to have a Gmail Account)'
        label = createDefaultMultiLineLabel(labelText)
        setMaxSizeForWidget(label, 120, 700)
        setDefaultFontForSettings(label)
        return label

    def createSenderToggle(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 0, 0)
        self.enableButton = self.createEnableButton()
        self.disableButton = self.createDisableButton()
        layout.addWidget(self.enableButton)
        layout.addWidget(self.disableButton)
        return layout

    def createEnableButton(self):
        button = QPushButton('Yes')
        button.clicked.connect(self.signals.showMenu.emit)
        button.setStyleSheet("background-color: #dfe4ea;")
        setMaxSizeForWidget(button, 30, 60)
        setDefaultFontForSettings(button)
        return button

    def createDisableButton(self):
        button = QPushButton('No')
        button.setObjectName('active')
        button.clicked.connect(self.signals.hideMenu.emit)
        button.setStyleSheet("background-color: #7bed9f;")
        setMaxSizeForWidget(button, 30, 60)
        setDefaultFontForSettings(button)
        return button

    def createSaveButton(self):
        box = QHBoxLayout()
        button = QPushButton('Save')
        button.clicked.connect(self.signals.saveSettings.emit)
        setMaxSizeForWidget(button, 35, 80)
        setDefaultFontForWidget(button)
        box.addWidget(button)
        return box

    def checkIfSenderIsActive(self):
        config = self.getCurrentConfig()
        if config.get('sender', 'is_active') == 'yes':
            self.signals.showMenu.emit()

    def showAdditionalMenu(self):
        self.setSenderEnableButtonAsActive()
        self.additionalLayout.setSpacing(30)
        self.additionalLayout.setContentsMargins(0, 0, 0, 230)
        currentConfig = self.getCurrentConfig()
        if currentConfig.get('sender', 'is_active') == 'yes':
            currEmail = currentConfig.get('sender', 'email')
            currPassword = currentConfig.get('sender', 'password')
            currTime = currentConfig.get('sender', 'time')
            if self.additionalLayout.count() == 0:
                self.additionalMenu = SettingsAdditionalMenuView(email=currEmail, password=currPassword, time=currTime)
        elif self.additionalLayout.count() == 0:
            self.additionalMenu = SettingsAdditionalMenuView()
        self.additionalLayout.addLayout(self.additionalMenu)

    def setSenderEnableButtonAsActive(self):
        self.enableButton.setObjectName('active')
        self.disableButton.setObjectName('')
        self.enableButton.setStyleSheet("background-color: #7bed9f;")
        self.disableButton.setStyleSheet("background-color: #dfe4ea;")

    def hideAdditionalMenu(self):
        self.setSenderDisableButtonAsActive()
        if self.additionalMenu.count() > 0:
            for i in reversed(range(self.additionalMenu.count())):
                self.additionalMenu.itemAt(i).widget().setParent(None)
            self.additionalLayout.itemAt(0).layout().setParent(None)

    def setSenderDisableButtonAsActive(self):
        self.enableButton.setObjectName('')
        self.disableButton.setObjectName('active')
        self.enableButton.setStyleSheet("background-color: #dfe4ea;")
        self.disableButton.setStyleSheet("background-color: #7bed9f;")

    def saveAllSettings(self):
        shortcutSettings = self.getShortcutSettings()
        senderSettings = None
        if self.enableButton.objectName() == 'active':
            if self.checkRequiredFields() is True:
                senderSettings = self.getSenderSettings()
        config = Config(shortcutSettings, senderSettings)
        config.saveToIniFile()
        # -> createKeyShortcuts in Windows
        # -> add scheduled task to Windows

    def getShortcutSettings(self):
        shortcuts = self.shortcutInput.keySequence()
        if shortcuts.count() > 0:
            tempList = shortcuts.toString().split(', ')
            shortcutsList = []
            for shortcut in tempList:
                if shortcut not in shortcutsList:
                    shortcutsList.append(shortcut)
            return shortcutsList
        else:
            return None

    def checkRequiredFields(self):
        email = self.additionalMenu.emailAddressInput.text()
        password = self.additionalMenu.appPasswordInput.text()
        if len(email) > 0 and len(password) > 0:
            return True
        else:
            requirementsDialog = RequirementsDialog(email, password)
            requirementsDialog.exec()
            return False

    def getSenderSettings(self):
        email = self.additionalMenu.emailAddressInput.text()
        password = self.additionalMenu.appPasswordInput.text()
        time = self.additionalMenu.timeSetterInput.text()
        senderSettings = {
            'email': email,
            'password': password,
            'time': time,
        }
        return senderSettings
