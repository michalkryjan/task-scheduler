from datetime import date
from PyQt5.QtWidgets import qApp
from .DefaultOneTaskView import DefaultOneTaskView
from database.DbActions import addTaskToDb


class NewTaskView(DefaultOneTaskView):
    def __init__(self, statusBar, refreshMethod):
        super().__init__()
        self.statusBar = statusBar
        self.refreshWindow = refreshMethod
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
        priority = self.priority.currentText()
        addTaskToDb(title, description, deadline, priority)
        self.refreshWindow()
        self.statusBar.msgTaskAdded()
