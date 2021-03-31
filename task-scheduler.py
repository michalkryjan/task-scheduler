from PyQt5.QtWidgets import qApp, QMainWindow, QApplication, QWidget, QFormLayout, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QDateEdit, QComboBox, QPushButton, QTabWidget, QScrollArea, QGroupBox, QDialog
from PyQt5.QtCore import Qt, QDate, QDateTime, QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap
import sys, os
from dbActions import addTaskToDb, startDb
from Task import Task
from getTasks import getAll, getForToday, getForTomorrow, getUrgent, getNotUrgent, getDone, getOne
from datetime import date, datetime


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        startDb()
        self.setWindowTitle('Task scheduler')
        self.setWindowIcon(QIcon('icons/tasks_icon.png'))
        self.tab_widget = TabWidget(self)
        self.setCentralWidget(self.tab_widget)
        self.resize(800, 700)
        self.setMaximumHeight(700)
        self.setMaximumWidth(800)
        self.setMinimumWidth(800)
        self.show()


class TabWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent) 
        self.layout = QVBoxLayout()  
        self.createTabs()

    def createTabs(self):
        # font for tabs
        font = QFont()
        font.setFamily('Century Gothic')
        font.setPointSize(9)
        # tab screen
        self.tabs = QTabWidget()
        self.tabs.setFont(font)
        self.newTask = QWidget()
        self.checkYourTasks = QTabWidget()
        self.allTasks = QWidget()
        self.forTodayTasks = QWidget()
        self.forTomorrowTasks = QWidget()
        self.urgentTasks = QWidget()
        self.notUrgentTasks = QWidget()
        self.doneTasks = QWidget()
        # add tabs
        self.tabs.addTab(self.newTask, 'New Task')
        self.tabs.addTab(self.checkYourTasks, 'Check your tasks')
        self.checkYourTasks.addTab(self.forTodayTasks, 'For today')
        self.checkYourTasks.addTab(self.forTomorrowTasks, 'For tomorrow')
        self.checkYourTasks.addTab(self.urgentTasks, 'Urgent')
        self.checkYourTasks.addTab(self.notUrgentTasks, 'Not urgent')
        self.checkYourTasks.addTab(self.allTasks, 'All to do')
        self.checkYourTasks.addTab(self.doneTasks, 'Done')
        # creating views for tabs
        self.newTaskView()
        self.allTasksView()
        self.forTodayTasksView()
        self.forTomorrowTasksView()
        self.urgentTasksView()
        self.notUrgentTasksView()
        self.doneTasksView()
        # add tabs to layout 
        self.layout.addWidget(self.tabs) 
        self.setLayout(self.layout)

    def newTaskView(self):
        # customized fonts
        font1 = QFont()
        font1.setFamily('Sitka Small')
        font1.setPointSize(20)
        font2 = QFont()
        font2.setFamily('Sitka Small')
        font2.setPointSize(11)
        # main layouts
        self.newTask.outerLayout = QVBoxLayout(self)
        self.newTask.middleFormLayout = QFormLayout()
        self.newTask.bottomLayout = QHBoxLayout()
        # main title of tab
        self.newtask_label = QLabel('Add a new task')
        self.newtask_label.setFont(font1)
        self.newTask.outerLayout.addWidget(self.newtask_label, alignment=Qt.AlignCenter)
        # title
        self.title = QLineEdit()
        self.title.setObjectName('title')
        self.title_label = QLabel('Title:')
        self.title.setFont(font2)
        self.title_label.setFont(font2)
        self.title.setMaxLength(100)
        self.title.setMaximumWidth(640)
        self.newTask.middleFormLayout.addRow(self.title_label, self.title)
        # description
        self.description = QTextEdit()
        self.description_label = QLabel('Description:')
        self.description.setObjectName('description')
        self.description.setFont(font2)
        self.description_label.setFont(font2)
        self.description.setMaximumHeight(200)
        self.description.setMaximumWidth(640)
        self.newTask.middleFormLayout.addRow(self.description_label, self.description)
        # deadline
        self.deadline = QDateEdit()
        self.deadline.setObjectName('deadline')
        self.deadline_label = QLabel('Deadline:')
        self.deadline_label.setFont(font2)
        self.deadline.setFont(font2)
        self.deadline.setMaximumHeight(40)
        self.deadline.setMaximumWidth(130)
        self.deadline.setDateTime(QDateTime.currentDateTime())
        self.deadline.setMaximumDate(QDate(2100, 12, 28))
        self.deadline.setCalendarPopup(True)
        self.deadline.setFocusPolicy(Qt.ClickFocus)
        self.newTask.middleFormLayout.addRow(self.deadline_label, self.deadline)
        # is urgent
        self.isurgent = QComboBox()
        self.isurgent.setObjectName('isurgent')
        self.isurgent_label = QLabel('Is urgent?')
        self.isurgent_label.setFont(font2)
        self.isurgent.setFont(font2)
        self.isurgent.setMaximumHeight(40)
        self.isurgent.setMaximumWidth(130)
        self.isurgent.addItem('Yes')
        self.isurgent.addItem('No')
        self.newTask.middleFormLayout.addRow(self.isurgent_label, self.isurgent)
        # save
        self.save = QPushButton('Save')
        self.save.setObjectName('save')
        self.save.setFont(font2)
        self.save.setMaximumHeight(100)
        self.save.setMaximumWidth(150)
        self.save.clicked.connect(self.saveNewTask)
        self.newTask.bottomLayout.addWidget(self.save)
        # close
        self.close = QPushButton('Close')
        self.close.setObjectName('close')
        self.close.setFont(font2)
        self.close.setMaximumHeight(100)
        self.close.setMaximumWidth(150)
        self.close.clicked.connect(qApp.quit)
        self.newTask.bottomLayout.addWidget(self.close)
        # connecting layouts
        self.newTask.outerLayout.addLayout(self.newTask.middleFormLayout)
        self.newTask.outerLayout.addLayout(self.newTask.bottomLayout)
        self.newTask.setLayout(self.newTask.outerLayout)

    def createTaskList(self, tasks):
        groupboxLayout = QVBoxLayout()
        for task in tasks:
            row = QHBoxLayout()
            row.setSpacing(20)
            row.setAlignment(Qt.AlignTop)
            # category dot
            squareIcon = QLabel()
            if task.status == 'done':
                squareIcon.setPixmap(QPixmap('icons/green_square.png'))
            else:
                if task.is_urgent == 'Yes':
                    squareIcon.setPixmap(QPixmap('icons/red_square.png'))
                else:
                    squareIcon.setPixmap(QPixmap('icons/yellow_square.png'))
            row.addWidget(squareIcon)
            # task name
            name = QLabel(task.name)
            name.setMaximumHeight(50)
            name.setMinimumHeight(50)
            name.setFixedWidth(400)
            name.setWordWrap(True)
            row.addWidget(name)
            # task deadline
            deadline = QLabel(task.deadline)
            deadline.setMinimumWidth(70)
            deadline.setMaximumWidth(70)
            row.addWidget(deadline)
            # check details button
            check = QPushButton('Check details')
            check.setMaximumWidth(110)
            check.setObjectName(str(task.id)) 
            check.clicked.connect(self.checkDetails)
            row.addWidget(check)
            # task done button
            if task.status == 'new':
                taskDone = QPushButton()
                taskDone.setIcon(QIcon('icons/check_icon.png'))
                taskDone.setIconSize(QSize(20,20))
                taskDone.setMaximumWidth(40)
                taskDone.setObjectName(str(task.id))
                taskDone.clicked.connect(self.setAsDone)
                row.addWidget(taskDone)
            # add task to the list
            groupboxLayout.addLayout(row)
        # add scroll to the list
        tasklist = QWidget()
        tasklist.setLayout(groupboxLayout)
        scroll = QScrollArea()
        scroll.setWidget(tasklist)
        scroll.setWidgetResizable(False)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        return scroll

    # views

    def allTasksView(self):
        tasks = getAll()
        taskList = self.createTaskList(tasks)
        self.allTasks.layout = QVBoxLayout()
        self.allTasks.layout.addWidget(taskList)
        self.allTasks.setLayout(self.allTasks.layout)
    
    def forTodayTasksView(self):
        tasks = getForToday()
        taskList = self.createTaskList(tasks)
        self.forTodayTasks.layout = QVBoxLayout()
        self.forTodayTasks.layout.addWidget(taskList)
        self.forTodayTasks.setLayout(self.forTodayTasks.layout)
    
    def forTomorrowTasksView(self):
        tasks = getForTomorrow()
        taskList = self.createTaskList(tasks)
        self.forTomorrowTasks.layout = QVBoxLayout()
        self.forTomorrowTasks.layout.addWidget(taskList)
        self.forTomorrowTasks.setLayout(self.forTomorrowTasks.layout)
    
    def urgentTasksView(self):
        tasks = getUrgent()
        taskList = self.createTaskList(tasks)
        self.urgentTasks.layout = QVBoxLayout()
        self.urgentTasks.layout.addWidget(taskList)
        self.urgentTasks.setLayout(self.urgentTasks.layout)

    def notUrgentTasksView(self):
        tasks = getNotUrgent()
        taskList = self.createTaskList(tasks)
        self.notUrgentTasks.layout = QVBoxLayout()
        self.notUrgentTasks.layout.addWidget(taskList)
        self.notUrgentTasks.setLayout(self.notUrgentTasks.layout)

    def doneTasksView(self):
        tasks = getDone()
        taskList = self.createTaskList(tasks)
        self.doneTasks.layout = QVBoxLayout()
        self.doneTasks.layout.addWidget(taskList)
        self.doneTasks.setLayout(self.doneTasks.layout)

    # events for buttons

    def checkDetails(self):
        sender = self.sender()
        id = sender.objectName()
        selectedTask = getOne(id)
        # open new window for editing task here
        self.details = QDialog()
        self.details.setWindowIcon(QIcon('icons/calendar_icon.png'))
        self.details.resize(800,700)
        self.details.setWindowTitle('Details')
        self.details.setWindowModality(Qt.ApplicationModal)
        # customized fonts
        font1 = QFont()
        font1.setFamily('Sitka Small')
        font1.setPointSize(20)
        font2 = QFont()
        font2.setFamily('Sitka Small')
        font2.setPointSize(11)
        # main layouts
        self.details.outerLayout = QVBoxLayout(self)
        self.details.middleFormLayout = QFormLayout()
        self.details.bottomLayout = QHBoxLayout()
        # main title of tab
        details_label = QLabel('Edit task')
        details_label.setFont(font1)
        self.details.outerLayout.addWidget(details_label, alignment=Qt.AlignCenter)
        # title
        self.currentTitle = QLineEdit(selectedTask.name)
        self.currentTitle.setObjectName('currentTitle')
        self.currentTitle.setFont(font2)
        self.currentTitle.setMaxLength(100)
        self.currentTitle.setMaximumWidth(640)
        title_label = QLabel('Title:')
        title_label.setFont(font2)
        self.details.middleFormLayout.addRow(title_label, self.currentTitle)
        # description
        self.currentDescription = QTextEdit(selectedTask.description)
        self.currentDescription.setObjectName('currentDescription')
        self.currentDescription.setFont(font2)
        self.currentDescription.setMaximumHeight(200)
        self.currentDescription.setMaximumWidth(640)
        description_label = QLabel('Description:')
        description_label.setFont(font2)
        self.details.middleFormLayout.addRow(description_label, self.currentDescription)
        # deadline
        d, m, y = map(int, selectedTask.deadline.split('.'))
        self.currentDeadline = QDateEdit(QDate(y, m, d))
        self.currentDeadline.setObjectName('currentDeadline')
        deadline_label = QLabel('Deadline:')
        deadline_label.setFont(font2)
        self.currentDeadline.setFont(font2)
        self.currentDeadline.setMaximumHeight(40)
        self.currentDeadline.setMaximumWidth(130)
        self.currentDeadline.setMaximumDate(QDate(2100, 12, 28))
        self.currentDeadline.setCalendarPopup(True)
        self.currentDeadline.setFocusPolicy(Qt.ClickFocus)
        self.details.middleFormLayout.addRow(deadline_label, self.currentDeadline)
        # is urgent
        self.currentIsurgent = QComboBox()
        isurgent_label = QLabel('Is urgent?')
        isurgent_label.setFont(font2)
        self.currentIsurgent.setFont(font2)
        self.currentIsurgent.setMaximumHeight(40)
        self.currentIsurgent.setMaximumWidth(130)
        self.currentIsurgent.addItem('Yes')
        self.currentIsurgent.addItem('No')
        self.currentIsurgent.setCurrentText(str(selectedTask.is_urgent))
        self.details.middleFormLayout.addRow(isurgent_label, self.currentIsurgent)
        # save
        self.currentSave = QPushButton('Save')
        self.currentSave.setObjectName(str(selectedTask.id))
        self.currentSave.setFont(font2)
        self.currentSave.setMaximumHeight(100)
        self.currentSave.setMaximumWidth(150)
        self.currentSave.clicked.connect(self.saveCurrentTask) 
        self.details.bottomLayout.addWidget(self.currentSave)
        # delete
        self.currentDelete = QPushButton('Delete')
        self.currentDelete.setObjectName(str(selectedTask.id))
        self.currentDelete.setFont(font2)
        self.currentDelete.setMaximumHeight(100)
        self.currentDelete.setMaximumWidth(150)
        self.currentDelete.clicked.connect(self.deleteCurrentTask)
        self.details.bottomLayout.addWidget(self.currentDelete)
        # close
        close = QPushButton('Close')
        close.setFont(font2)
        close.setMaximumHeight(100)
        close.setMaximumWidth(150)
        close.clicked.connect(self.details.close)
        self.details.bottomLayout.addWidget(close)
        # connecting layouts
        self.details.outerLayout.addLayout(self.details.middleFormLayout)
        self.details.outerLayout.addLayout(self.details.bottomLayout)
        self.details.setLayout(self.details.outerLayout)
        self.details.exec_()

    def saveNewTask(self):
        name = self.title.text()
        description = self.description.toPlainText()
        deadline = self.deadline.text()
        is_urgent = self.isurgent.currentText()
        addTaskToDb(name, description, deadline, is_urgent)
        self.refreshWindow()

    def saveCurrentTask(self):
        sender = self.sender()
        id = sender.objectName()
        oldTask = getOne(id)
        currentName = self.currentTitle.text()
        currentDescription = self.currentDescription.toPlainText()
        currentDeadline = self.currentDeadline.text()
        currentIsurgent = self.currentIsurgent.currentText()
        oldTask.updateTask(currentName, currentDescription, currentDeadline, currentIsurgent)
        self.refreshWindow()

    def deleteCurrentTask(self):
        sender = self.sender()
        id = sender.objectName()
        currentTask = getOne(id)
        self.details.close()
        currentTask.deleteTask()
        self.refreshWindow()

    def setAsDone(self):
        sender = self.sender()
        id = sender.objectName()
        task = getOne(id)
        task.setTaskAsDone()
        self.refreshWindow()

    def refreshWindow(self):
        firstIndex = self.tabs.currentIndex()
        if firstIndex == 1:
            secondIndex = self.checkYourTasks.currentIndex()
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().setParent(None)
        self.createTabs()
        if firstIndex == 1:
            self.tabs.setCurrentIndex(1)
            self.checkYourTasks.setCurrentIndex(secondIndex)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
