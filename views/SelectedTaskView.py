from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QPushButton
from .DefaultOneTaskView import DefaultOneTaskView
from Fonts import *


class SelectedTaskView(DefaultOneTaskView):
    def __init__(self, QDialogWindow, selectedTask, statusBar, refreshMethod):
        super().__init__()
        self.QDialogWindow = QDialogWindow
        self.selectedTask = selectedTask
        self.statusBar = statusBar
        self.refreshWindow = refreshMethod
        self.mainLabel.setText('Edit task')
        self.setCurrentDataForFields()
        self.deleteButton = self.createDeleteButton(self.footerLayout)
        self.setMethodsForButtons()

    def createDeleteButton(self, layout):
        button = QPushButton('Delete')
        button.setObjectName(str(self.selectedTask.id))
        button.setMaximumHeight(100)
        button.setMaximumWidth(150)
        setDefaultFontForWidget(button)
        layout.addWidget(button)
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
        self.refreshWindow()
        self.statusBar.msgTaskUpdated()

    def deleteTask(self):
        self.selectedTask.deleteTask()
        self.refreshWindow()
        self.QDialogWindow.close()
        self.statusBar.msgTaskDeleted()

    def setCurrentDataForFields(self):
        self.title.setText(self.selectedTask.name)
        self.description.setText(self.selectedTask.description)
        self.isurgent.setCurrentText(self.selectedTask.is_urgent)
        d, m, y = map(int, self.selectedTask.deadline.split('.'))
        self.deadline.setDate(QDate(y, m, d))
