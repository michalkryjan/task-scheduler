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
        self.additionalLayout = QFormLayout()
        self.addLayout(self.createMainLayout())
        self.addLayout(self.additionalLayout)
        self.addLayout(self.createSaveButton())
        self.signals.showMenu.connect(self.showAdditionalMenu)
        self.signals.hideMenu.connect(self.hideAdditionalMenu)

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
        field.setContentsMargins(10, 5, 0, 0)
        self.setMaxSizeForWidget(field, 70, 400)
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
        self.setMaxSizeForWidget(button, 30, 60)
        setSettingsDefaultFont(button)
        return button

    def createDisableButton(self):
        button = QPushButton('No')
        button.clicked.connect(self.signals.hideMenu.emit)
        button.setStyleSheet("background-color: #7bed9f;")
        self.setMaxSizeForWidget(button, 30, 60)
        setSettingsDefaultFont(button)
        return button

    def createSaveButton(self):
        box = QHBoxLayout()
        button = QPushButton('Save')
        self.setMaxSizeForWidget(button, 35, 80)
        setDefaultFontForWidget(button)
        box.addWidget(button)
        return box

    def showAdditionalMenu(self):
        self.enableButton.setStyleSheet("background-color: #7bed9f;")
        self.disableButton.setStyleSheet("background-color: #dfe4ea;")
        if self.additionalLayout.count() == 0:
            label = QLabel('Test label')
            setSettingsDefaultFont(label)
            self.additionalLayout.addRow(label)

    def hideAdditionalMenu(self):
        self.enableButton.setStyleSheet("background-color: #dfe4ea;")
        self.disableButton.setStyleSheet("background-color: #7bed9f;")
        if self.additionalLayout.count() != 0:
            for i in reversed(range(self.additionalLayout.count())):
                self.additionalLayout.itemAt(i).widget().setParent(None)

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
