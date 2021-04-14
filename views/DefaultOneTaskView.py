from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QFormLayout, QHBoxLayout, QLineEdit, QTextEdit, QDateEdit, QComboBox, \
    QPushButton
from Fonts import *


class DefaultOneTaskView(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.createMainLabel()
        self.addWidget(self.mainLabel, alignment=Qt.AlignCenter)
        self.addLayout(self.createBodyLayout())
        self.createFooterLayout()
        self.addLayout(self.footerLayout)

    def createMainLabel(self):
        self.mainLabel = QLabel()
        setBiggerFontForWidget(self.mainLabel)

    def createBodyLayout(self):
        self.title = self.createTitleField()
        self.description = self.createDescriptionField()
        self.deadline = self.createDeadlineField()
        self.isurgent = self.createIsUrgentField()
        bodyLayout = QFormLayout()
        bodyLayout.addRow(self.createDefaultLabel('Title:'), self.title)
        bodyLayout.addRow(self.createDefaultLabel('Description:'), self.description)
        bodyLayout.addRow(self.createDefaultLabel('Deadline:'), self.deadline)
        bodyLayout.addRow(self.createDefaultLabel('Is urgent?'), self.isurgent)
        return bodyLayout

    def createFooterLayout(self):
        self.saveButton = self.createSaveButton()
        self.closeButton = self.createCloseButton()
        self.footerLayout = QHBoxLayout()
        self.footerLayout.addWidget(self.saveButton)
        self.footerLayout.addWidget(self.closeButton)

    def createDefaultLabel(self, content):
        label = QLabel(content)
        setDefaultFontForWidget(label)
        return label

    def createTitleField(self):
        title = QLineEdit()
        title.setMaxLength(100)
        title.setMaximumWidth(640)
        setDefaultFontForWidget(title)
        return title

    def createDescriptionField(self):
        description = QTextEdit()
        description.setMaximumHeight(200)
        description.setMaximumWidth(640)
        setDefaultFontForWidget(description)
        return description

    def createDeadlineField(self):
        deadline = QDateEdit()
        deadline.setMaximumHeight(40)
        deadline.setMaximumWidth(130)
        deadline.setMaximumDate(QDate(2100, 12, 28))
        deadline.setCalendarPopup(True)
        deadline.setFocusPolicy(Qt.ClickFocus)
        setDefaultFontForWidget(deadline)
        return deadline

    def createIsUrgentField(self):
        isurgent = QComboBox()
        isurgent.setMaximumHeight(40)
        isurgent.setMaximumWidth(130)
        isurgent.addItem('Yes')
        isurgent.addItem('No')
        setDefaultFontForWidget(isurgent)
        return isurgent

    def createSaveButton(self):
        button = QPushButton('Save')
        button.setMaximumHeight(100)
        button.setMaximumWidth(150)
        setDefaultFontForWidget(button)
        return button

    def createCloseButton(self):
        button = QPushButton('Close')
        button.setMaximumHeight(100)
        button.setMaximumWidth(150)
        setDefaultFontForWidget(button)
        return button
