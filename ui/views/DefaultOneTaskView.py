from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QFormLayout, QHBoxLayout, QLineEdit, QTextEdit, QDateEdit, QComboBox, \
    QPushButton
from ..Fonts import *


class DefaultOneTaskView(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.mainLabel = self.createMainLabel()
        self.addWidget(self.mainLabel, alignment=Qt.AlignCenter)
        self.addLayout(self.createBodyLayout())
        self.footerLayout = self.createFooterLayout()
        self.addLayout(self.footerLayout)

    def createMainLabel(self):
        mainLabel = QLabel()
        setBiggerFontForWidget(mainLabel)
        return mainLabel

    def createBodyLayout(self):
        bodyLayout = QFormLayout()
        self.title = self.createTitleField()
        self.description = self.createDescriptionField()
        self.deadline = self.createDeadlineField()
        self.priority = self.createPriorityField()
        bodyLayout.addRow(self.createDefaultLabel('Title:'), self.title)
        bodyLayout.addRow(self.createDefaultLabel('Description:'), self.description)
        bodyLayout.addRow(self.createDefaultLabel('Deadline:'), self.deadline)
        bodyLayout.addRow(self.createDefaultLabel('Priority:'), self.priority)
        return bodyLayout

    def createFooterLayout(self):
        footerLayout = QHBoxLayout()
        self.saveButton = self.createSaveButton()
        self.closeButton = self.createCloseButton()
        footerLayout.addWidget(self.saveButton)
        footerLayout.addWidget(self.closeButton)
        return footerLayout

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

    def createPriorityField(self):
        priority = QComboBox()
        priority.setMaximumHeight(40)
        priority.setMaximumWidth(130)
        for i in range(1, 5, 1):
            priority.addItem(f'{i}')
        setDefaultFontForWidget(priority)
        return priority

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
