from PyQt5.QtCore import QObject, pyqtSignal, Qt
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
        mainLayout.addRow(self.createShortcutLabel(), self.createShortcutField())
        mainLayout.addItem(QSpacerItem(0, 20))
        mainLayout.addRow(self.createSenderToggleLabel(), self.createSenderToggle())
        return mainLayout

    def createShortcutLabel(self):
        labelText = 'Set shortcut keys for opening the app with the view of adding a new task at any moment:'
        label = self.createDefaultMultiLineLabel(labelText)
        label.setMaximumHeight(120)
        label.setMaximumWidth(700)
        setSettingsDefaultFont(label)
        return label

    def createShortcutField(self):
        field = QKeySequenceEdit()
        self.setMaxSizeForWidget(field, 70, 300)
        setSettingsDefaultFont(field)
        return field

    def createSenderToggleLabel(self):
        labelText = 'Enable email sender feature? \n(you need to have a Gmail Account)'
        label = self.createDefaultMultiLineLabel(labelText)
        self.setMaxSizeForWidget(label, 120, 700)
        setSettingsDefaultFont(label)
        return label

    def createSenderToggle(self):
        layout = QHBoxLayout()
        layout.addWidget(self.createEnableButton())
        layout.addWidget(self.createDisableButton())
        return layout

    def createEnableButton(self):
        button = QPushButton('Yes')
        self.setMaxSizeForWidget(button, 30, 60)
        setSettingsDefaultFont(button)
        return button

    def createDisableButton(self):
        button = QPushButton('No')
        self.setMaxSizeForWidget(button, 30, 60)
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
