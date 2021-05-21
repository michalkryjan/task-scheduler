from PyQt5.QtCore import QObject, pyqtSignal, Qt
from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QHBoxLayout, QPushButton, QKeySequenceEdit, QSpacerItem
from ..Defaults import *
from .SettingsAdditionalMenuView import SettingsAdditionalMenuView


class SettingsSignals(QObject):
    showMenu = pyqtSignal()
    hideMenu = pyqtSignal()


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

    def createMainLayout(self):
        mainLayout = QFormLayout()
        mainLayout.addRow(self.createShortcutLabel(), self.createShortcutField())
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
        field = QKeySequenceEdit()
        field.setContentsMargins(10, 5, 0, 0)
        setMaxSizeForWidget(field, 70, 400)
        setDefaultFontForSettings(field)
        return field

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
        button.clicked.connect(self.signals.hideMenu.emit)
        button.setStyleSheet("background-color: #7bed9f;")
        setMaxSizeForWidget(button, 30, 60)
        setDefaultFontForSettings(button)
        return button

    def createSaveButton(self):
        box = QHBoxLayout()
        button = QPushButton('Save')
        setMaxSizeForWidget(button, 35, 80)
        setDefaultFontForWidget(button)
        box.addWidget(button)
        return box

    def showAdditionalMenu(self):
        self.enableButton.setStyleSheet("background-color: #7bed9f;")
        self.disableButton.setStyleSheet("background-color: #dfe4ea;")
        self.additionalLayout.setSpacing(30)
        self.additionalLayout.setContentsMargins(0, 0, 0, 230)
        if self.additionalLayout.count() == 0:
            self.additionalMenu = SettingsAdditionalMenuView()
            self.additionalLayout.addLayout(self.additionalMenu)

    def hideAdditionalMenu(self):
        self.enableButton.setStyleSheet("background-color: #dfe4ea;")
        self.disableButton.setStyleSheet("background-color: #7bed9f;")
        if self.additionalMenu.count() > 0:
            for i in reversed(range(self.additionalMenu.count())):
                self.additionalMenu.itemAt(i).widget().setParent(None)
            self.additionalLayout.itemAt(0).layout().setParent(None)
