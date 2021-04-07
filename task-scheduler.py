from PyQt5.QtWidgets import qApp, QMainWindow, QApplication, QWidget, QFormLayout, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QDateEdit, QComboBox, QPushButton, QTabWidget, QScrollArea, QGroupBox, QDialog
from PyQt5.QtCore import Qt, QDate, QDateTime, QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap
import sys, os
from dbActions import addTaskToDb, startDb
from Task import Task
from getTasks import getAll, getForToday, getForTomorrow, getUrgent, getNotUrgent, getDone, getOne
from datetime import date, datetime
from Views import *


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        startDb()
        self.setWindowTitle('Task scheduler')
        self.setWindowIcon(QIcon('icons/tasks_icon.png'))
        self.tabWidget = TabWidget(self)
        self.setCentralWidget(self.tabWidget)
        self.setWindowSize()
        self.show()

    def setWindowSize(self):
        self.resize(800, 700)
        self.setMaximumHeight(700)
        self.setMaximumWidth(800)
        self.setMinimumWidth(800)


class TabWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent) 
        self.layout = QVBoxLayout()  
        self.tabs = self.createTabs()
        self.setLayout(self.layout)

    def createTabs(self):
        tabs = QTabWidget()
        self.setFontForTabs(tabs)
        self.checkYourTasks = self.InitTabScreen(tabs)
        self.layout.addWidget(tabs) 
        return tabs

    def setFontForTabs(self, tabs):
        font = QFont()
        font.setFamily('Century Gothic')
        font.setPointSize(9)
        tabs.setFont(font)

    def InitTabScreen(self, tabs):
        TabScreen = QTabWidget()
        newTask = self.createWidgetUnder(tabs, 'New Task')
        self.InitNewTaskView(newTask)
        tabs.addTab(TabScreen, 'Check your tasks')
        allTasks = self.createWidgetWithViewUnder(TabScreen, 'All to do', getAll)
        forTodayTasks = self.createWidgetWithViewUnder(TabScreen, 'For today', getForToday)
        forTomorrowTasks = self.createWidgetWithViewUnder(TabScreen, 'For tomorrow', getForTomorrow)
        urgentTasks = self.createWidgetWithViewUnder(TabScreen, 'Urgent', getUrgent)
        notUrgentTasks = self.createWidgetWithViewUnder(TabScreen, 'Not urgent', getNotUrgent)
        doneTasks = self.createWidgetWithViewUnder(TabScreen, 'Done', getDone)
        return TabScreen

    def InitNewTaskView(self, newTask):
        newTaskView = NewTaskView(self)
        newTask.setLayout(newTaskView)

    def createWidgetUnder(self, parentTab, name):
        widget = QWidget()
        parentTab.addTab(widget, name)
        return widget

    def createWidgetWithViewUnder(self, parentTab, name, getTasksMethod):
        widget = QWidget()
        parentTab.addTab(widget, name)
        self.createTabView(widget, getTasksMethod)
        return widget

    def createTabView(self, widget, getTasksMethod):
        tasks = getTasksMethod()
        taskList = self.createTaskList(tasks)
        layout = QVBoxLayout()
        layout.addWidget(taskList)
        widget.setLayout(layout)

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
            categoryIcon.setPixmap(QPixmap('icons/green_square.png'))
        else:
            if task.is_urgent == 'Yes':
                categoryIcon.setPixmap(QPixmap('icons/red_square.png'))
            else:
                categoryIcon.setPixmap(QPixmap('icons/yellow_square.png'))
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
        detailsWindow = QDialog()
        sender = self.sender()
        selectedTask = getOne(sender.objectName())
        selectedTaskView = SelectedTaskView(self, detailsWindow, selectedTask)
        
        detailsWindow.setLayout(selectedTaskView)
        detailsWindow.setWindowIcon(QIcon('icons/calendar_icon.png'))
        detailsWindow.resize(800,700)
        detailsWindow.setWindowTitle('Details')
        detailsWindow.setWindowModality(Qt.ApplicationModal)
        detailsWindow.exec_()

    def createTaskDoneButton(self, task):
        button = QPushButton()
        button.setIcon(QIcon('icons/check_icon.png'))
        button.setIconSize(QSize(20,20))
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
        id = sender.objectName()
        task = getOne(id)
        task.setTaskAsDone()
        self.refreshWindow()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
