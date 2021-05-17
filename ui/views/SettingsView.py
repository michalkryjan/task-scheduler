from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QFormLayout, QHBoxLayout, QLineEdit, QTextEdit, QDateEdit, QComboBox, \
    QPushButton, QKeySequenceEdit, QSpacerItem
from ..Fonts import *


class SettingsSignals(QObject):
    showMenu = pyqtSignal()
    hideMenu = pyqtSignal()


class SettingsView(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.signals = SettingsSignals()
        self.addLayout(self.createMainLayout())
        self.addLayout(self.createAdditionalLayout())
        self.saveButton = self.createSaveButton()

    def createMainLayout(self):
        mainLayout = QFormLayout()
        self.shortcutField = self.createShortcutField()
        self.senderEnableButton = self.createEnableButton()
        self.senderDisableButton = self.createDisableButton()
        mainLayout.addRow(self.createShortcutLabel(), self.shortcutField)
        mainLayout.addItem(QSpacerItem(0, 20))
        mainLayout.addRow(self.createSenderToggleLabel())
        mainLayout.addRow(self.senderEnableButton, self.senderDisableButton)
        return mainLayout

    def createShortcutLabel(self):
        labelText = 'Set shortcut keys for opening the app with the view of adding a new task at any moment:'
        label = self.createDefaultMultiLineLabel(labelText)
        label.setMaximumHeight(120)
        label.setMaximumWidth(700)
        setSettingsDefaultFont(label)
        return label

    def createSenderToggleLabel(self):
        labelText = 'Enable email sender feature? \n(you need to have a Gmail Account)'
        label = self.createDefaultMultiLineLabel(labelText)
        label.setMaximumHeight(120)
        label.setMaximumWidth(700)
        setSettingsDefaultFont(label)
        return label

    def createShortcutField(self):
        field = QKeySequenceEdit()
        field.setMaximumHeight(70)
        field.setMaximumWidth(300)
        setSettingsDefaultFont(field)
        return field

    def createEnableButton(self):
        button = QPushButton('Yes')
        button.setMaximumHeight(30)
        button.setMaximumWidth(60)
        setSettingsDefaultFont(button)
        return button

    def createDisableButton(self):
        button = QPushButton('No')
        button.setMaximumHeight(30)
        button.setMaximumWidth(60)
        setSettingsDefaultFont(button)
        return button

    def createAdditionalLayout(self):
        additionalLayout = QFormLayout()
        return additionalLayout

    def createSaveButton(self):
        saveButton = QPushButton()
        return saveButton

    def createDefaultOneLineLabel(self, content):
        label = QLabel(content)
        setSettingsDefaultFont(label)
        return label

    def createDefaultMultiLineLabel(self, content):
        label = QLabel(content)
        setSettingsDefaultFont(label)
        label.setWordWrap(True)
        return label

    def setMaxSizeForWidget(self, widget, height, width):
        widget.setMaximumHeight(height)
        widget.setMaximumWidth(width)

    def setMinSizeForWidget(self, widget, height, width):
        widget.setMinimumHeight(height)
        widget.setMinimumWidth(width)
