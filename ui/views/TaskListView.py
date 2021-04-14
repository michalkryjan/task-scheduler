from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDialog, QWidget, QScrollArea
from database.GetTasks import *
from .SelectedTaskView import SelectedTaskView
import os


currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)


class TaskListView(QVBoxLayout):
    def __init__(self, tasks, statusBar, refreshMethod):
        super().__init__()
        self.statusBar = statusBar
        taskList = self.createTaskList(tasks)
        self.addWidget(taskList)
        self.refreshWindow = refreshMethod

    def createTaskList(self, tasks):
        mainLayout = QVBoxLayout()
        for currentTask in tasks:
            row = QHBoxLayout()
            row.setSpacing(20)
            row.setAlignment(Qt.AlignTop)
            row.addWidget(self.createCategoryIcon(currentTask))
            row.addWidget(self.createTaskNameInfo(currentTask))
            row.addWidget(self.createTaskDeadlineInfo(currentTask))
            row.addWidget(self.createCheckDetailsButton(currentTask))
            if currentTask.status == 'new':
                row.addWidget(self.createTaskDoneButton(currentTask))
            mainLayout.addLayout(row)
        scrollTaskList = self.createScrollTaskList(mainLayout)
        return scrollTaskList

    def createCategoryIcon(self, task):
        categoryIcon = QLabel()
        if task.status == 'done':
            categoryIcon.setPixmap(QPixmap(f'{parentdir}/icons/green_square.png'))
        else:
            if task.is_urgent == 'Yes':
                categoryIcon.setPixmap(QPixmap(f'{parentdir}/icons/red_square.png'))
            else:
                categoryIcon.setPixmap(QPixmap(f'{parentdir}/icons/yellow_square.png'))
        return categoryIcon

    def createTaskNameInfo(self, task):
        name = QLabel(task.name)
        name.setMaximumHeight(50)
        name.setMinimumHeight(50)
        name.setFixedWidth(400)
        name.setWordWrap(True)
        return name

    def createTaskDeadlineInfo(self, task):
        deadline = QLabel(task.deadline)
        deadline.setMinimumWidth(70)
        deadline.setMaximumWidth(70)
        return deadline

    def createCheckDetailsButton(self, task):
        button = QPushButton('Check details')
        button.setMaximumWidth(110)
        button.setObjectName(str(task.id))
        button.clicked.connect(self.InitSelectedTaskView)
        return button

    def InitSelectedTaskView(self):
        detailsWindow = self.createDetailsWindow()
        sender = self.sender()
        selectedTask = selectOneTask(sender.objectName())
        selectedTaskView = SelectedTaskView(detailsWindow, selectedTask, self.statusBar, self.refreshWindow)
        detailsWindow.setLayout(selectedTaskView)
        detailsWindow.exec_()

    def createDetailsWindow(self):
        window = QDialog()
        window.setWindowIcon(QIcon(f'{parentdir}/icons/calendar_icon.png'))
        window.resize(800, 700)
        window.setWindowTitle('Details')
        window.setWindowModality(Qt.ApplicationModal)
        return window

    def createTaskDoneButton(self, task):
        button = QPushButton()
        button.setIcon(QIcon(f'{parentdir}/icons/check_icon.png'))
        button.setIconSize(QSize(20, 20))
        button.setMaximumWidth(40)
        button.setObjectName(str(task.id))
        button.clicked.connect(self.setAsDone)
        return button

    def createScrollTaskList(self, layout):
        widget = QWidget()
        widget.setLayout(layout)
        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(False)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        return scroll

    def setAsDone(self):
        sender = self.sender()
        task = selectOneTask(sender.objectName())
        task.setTaskAsDone()
        self.refreshWindow()
        self.statusBar.msgTaskDone()
