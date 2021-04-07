from PyQt5.QtWidgets import qApp, QMainWindow, QApplication, QWidget, QFormLayout, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QDateEdit, QComboBox, QPushButton, QTabWidget, QScrollArea, QGroupBox, QDialog
from PyQt5.QtCore import Qt, QDate, QDateTime, QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap
import sys, os
from dbActions import addTaskToDb, startDb
from Task import Task
from getTasks import getAll, getForToday, getForTomorrow, getUrgent, getNotUrgent, getDone, getOne
from datetime import date, datetime


class DefaultTaskView(QVBoxLayout):
    def __init__(self, parent):
        super().__init__(parent) 
        self.createMainLabel()
        self.addWidget(self.mainLabel, alignment=Qt.AlignCenter)
        self.addLayout(self.createBodyLayout())
        self.createFooterLayout()
        self.addLayout(self.footerLayout)

    def createMainLabel(self):
        self.mainLabel = QLabel()
        self.setBiggerFontForWidget(self.mainLabel)

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

    def setDefaultFontForWidget(self, widget):
        font = QFont()
        font.setFamily('Sitka Small')
        font.setPointSize(11)
        widget.setFont(font)

    def setBiggerFontForWidget(self, widget):
        font = QFont()
        font.setFamily('Sitka Small')
        font.setPointSize(20)
        widget.setFont(font)

    def createDefaultLabel(self, content):
        label = QLabel(content)
        self.setDefaultFontForWidget(label)
        return label

    def createTitleField(self):
        title = QLineEdit()
        title.setMaxLength(100)
        title.setMaximumWidth(640)
        self.setDefaultFontForWidget(title)
        return title
    
    def createDescriptionField(self):
        description = QTextEdit()
        self.setDefaultFontForWidget(description)
        description.setMaximumHeight(200)
        description.setMaximumWidth(640)
        return description

    def createDeadlineField(self):
        deadline = QDateEdit()
        self.setDefaultFontForWidget(deadline)
        deadline.setMaximumHeight(40)
        deadline.setMaximumWidth(130)
        deadline.setMaximumDate(QDate(2100, 12, 28))
        deadline.setCalendarPopup(True)
        deadline.setFocusPolicy(Qt.ClickFocus)
        return deadline

    def createIsUrgentField(self):
        isurgent = QComboBox()
        self.setDefaultFontForWidget(isurgent)
        isurgent.setMaximumHeight(40)
        isurgent.setMaximumWidth(130)
        isurgent.addItem('Yes')
        isurgent.addItem('No')
        return isurgent

    def createSaveButton(self):
        button = QPushButton('Save')
        self.setDefaultFontForWidget(button)
        button.setMaximumHeight(100)
        button.setMaximumWidth(150)
        return button

    def createCloseButton(self):
        button = QPushButton('Close')
        self.setDefaultFontForWidget(button)
        button.setMaximumHeight(100)
        button.setMaximumWidth(150)
        return button


class NewTaskView(DefaultTaskView):
    def __init__(self, parent):
        super().__init__(parent) 
        self.setMethodsForButtons()
        self.mainLabel.setText('Add a new task')
        self.deadline.setDate(date.today())

    def setMethodsForButtons(self):
        self.saveButton.clicked.connect(self.saveNewTask)
        self.closeButton.clicked.connect(qApp.quit)

    def saveNewTask(self):
        title = self.title.text()
        description = self.description.toPlainText()
        deadline = self.deadline.text()
        isurgent = self.isurgent.currentText()
        addTaskToDb(title, description, deadline, isurgent)


class SelectedTaskView(DefaultTaskView):
    def __init__(self, parent, QDialogWindow, selectedTask):
        super().__init__(parent) 
        self.selectedTask = selectedTask
        self.QDialogWindow = QDialogWindow
        self.mainLabel.setText('Edit task')
        self.setCurrentDataForFields()
        self.deleteButton = self.createDeleteButton()
        self.setMethodsForButtons()

    def createDeleteButton(self):
        button = QPushButton('Delete')
        button.setObjectName(str(self.selectedTask.id))
        self.setDefaultFontForWidget(button)
        button.setMaximumHeight(100)
        button.setMaximumWidth(150)
        return button

    def setMethodsForButtons(self):
        self.saveButton.clicked.connect(self.saveSelectedTask)
        self.closeButton.clicked.connect(self.QDialogWindow.close)
        self.deleteButton.clicked.connect(self.deleteTask)

    def saveSelectedTask(self):
        title = self.title.text()
        description = self.description.toPlainText()
        deadline = self.deadline.text()
        isurgent = self.isurgent.currentText()
        self.selectedTask.updateTask(title, description, deadline, isurgent)

    def deleteTask(self):
        self.selectedTask.deleteTask()
        self.close()

    def setCurrentDataForFields(self):
        self.title.setText(self.selectedTask.name)
        self.description.setText(self.selectedTask.description)
        self.isurgent.setCurrentText(self.selectedTask.is_urgent)
        d, m, y = map(int, self.selectedTask.deadline.split('.'))
        self.deadline.setDate(QDate(y, m, d))
