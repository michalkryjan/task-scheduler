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

    def InitNewTaskView(self, newTask):
        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.createTaskMainLabel('Add a new task'), alignment=Qt.AlignCenter)
        mainLayout.addLayout(self.createNewTaskBodyLayout())
        mainLayout.addLayout(self.createNewTaskFooterLayout())
        newTask.setLayout(mainLayout)

    def createNewTaskBodyLayout(self):
        self.title = self.createTitleField('')
        self.description = self.createDescriptionField('')
        self.deadline = self.createDeadlineField(QDateTime.currentDateTime())
        self.isurgent = self.createIsUrgentField('')
        bodyLayout = QFormLayout()
        bodyLayout.addRow(self.createDefaultLabel('Title:'), self.title)
        bodyLayout.addRow(self.createDefaultLabel('Description:'), self.description)
        bodyLayout.addRow(self.createDefaultLabel('Deadline:'), self.deadline)
        bodyLayout.addRow(self.createDefaultLabel('Is urgent?'), self.isurgent)
        return bodyLayout

    def createNewTaskFooterLayout(self):
        save = self.createSaveButton('', self.saveNewTask)
        close = self.createCloseButton(qApp.quit)
        footerLayout = QHBoxLayout()
        footerLayout.addWidget(save)
        footerLayout.addWidget(close)
        return footerLayout

    def createDefaultLabel(self, content):
        label = QLabel(content)
        self.setDefaultFontForWidget(label)
        return label

    def createTaskMainLabel(self, content):
        label = QLabel(content)
        self.setBiggerFontForWidget(label)
        return label

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

    def createTitleField(self, content):
        title = QLineEdit(content)
        title.setMaxLength(100)
        title.setMaximumWidth(640)
        self.setDefaultFontForWidget(title)
        return title
    
    def createDescriptionField(self, content):
        description = QTextEdit(content)
        self.setDefaultFontForWidget(description)
        description.setMaximumHeight(200)
        description.setMaximumWidth(640)
        return description

    def createDeadlineField(self, content):
        deadline = QDateEdit()
        self.setDefaultFontForWidget(deadline)
        deadline.setMaximumHeight(40)
        deadline.setMaximumWidth(130)
        deadline.setDateTime(content)
        deadline.setMaximumDate(QDate(2100, 12, 28))
        deadline.setCalendarPopup(True)
        deadline.setFocusPolicy(Qt.ClickFocus)
        return deadline

    def createIsUrgentField(self, content):
        isurgent = QComboBox()
        self.setDefaultFontForWidget(isurgent)
        isurgent.setMaximumHeight(40)
        isurgent.setMaximumWidth(130)
        isurgent.addItem('Yes')
        isurgent.addItem('No')
        isurgent.setCurrentText(content)
        return isurgent

    def createSaveButton(self, buttonName, saveTaskMethod):
        save = QPushButton('Save')
        save.setObjectName(buttonName)
        self.setDefaultFontForWidget(save)
        save.setMaximumHeight(100)
        save.setMaximumWidth(150)
        save.clicked.connect(saveTaskMethod)
        return save

    def createCloseButton(self, closeMethod):
        close = QPushButton('Close')
        self.setDefaultFontForWidget(close)
        close.setMaximumHeight(100)
        close.setMaximumWidth(150)
        close.clicked.connect(closeMethod)
        return close

    def saveNewTask(self):
        name = self.title.text()
        description = self.description.toPlainText()
        deadline = self.deadline.text()
        is_urgent = self.isurgent.currentText()
        addTaskToDb(name, description, deadline, is_urgent)
        self.refreshWindow()

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


    def InitSelectedTaskView(self):
        sender = self.sender()
        id = sender.objectName()
        selectedTask = getOne(id)
        self.detailsWindow = QDialog()
        self.detailsWindow.setWindowIcon(QIcon('icons/calendar_icon.png'))
        self.detailsWindow.resize(800,700)
        self.detailsWindow.setWindowTitle('Details')
        self.detailsWindow.setWindowModality(Qt.ApplicationModal)
        self.detailsWindow.setLayout(self.createSelectedTaskLayout(selectedTask))
        self.detailsWindow.exec_()

    def createSelectedTaskLayout(self, selectedTask):
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.createTaskMainLabel('Edit task'), alignment=Qt.AlignCenter)
        mainLayout.addLayout(self.createSelectedTaskBodyLayout(selectedTask))
        mainLayout.addLayout(self.createSelectedTaskFooterLayout(selectedTask))
        return mainLayout

    def createSelectedTaskBodyLayout(self, selectedTask):
        self.currentTitle = self.createTitleField(selectedTask.name)
        self.currentDescription = self.createDescriptionField(selectedTask.description)
        self.currentDeadline = self.createDeadlineFieldAndSetDate(selectedTask)
        self.currentIsUrgent = self.createIsUrgentField(selectedTask.is_urgent)
        bodyLayout = QFormLayout()
        bodyLayout.addRow(self.createDefaultLabel('Title:'), self.currentTitle)
        bodyLayout.addRow(self.createDefaultLabel('Description:'), self.currentDescription)
        bodyLayout.addRow(self.createDefaultLabel('Deadline:'), self.currentDeadline)
        bodyLayout.addRow(self.createDefaultLabel('Is urgent?'), self.currentIsUrgent)
        return bodyLayout

    def createSelectedTaskFooterLayout(self, selectedTask):
        save = self.createSaveButton(str(selectedTask.id),self.saveCurrentTask)
        close = self.createCloseButton(self.detailsWindow.close)
        delete = self.createDeleteTaskButton(str(selectedTask.id))
        footerLayout = QHBoxLayout()
        footerLayout.addWidget(save)
        footerLayout.addWidget(close)
        footerLayout.addWidget(delete)
        return footerLayout

    def createDeadlineFieldAndSetDate(self, selectedTask):
        d, m, y = map(int, selectedTask.deadline.split('.'))
        deadlineField = QDateEdit(QDate(y, m, d))
        self.setDefaultFontForWidget(deadlineField)
        deadlineField.setMaximumHeight(40)
        deadlineField.setMaximumWidth(130)
        deadlineField.setMaximumDate(QDate(2100, 12, 28))
        deadlineField.setCalendarPopup(True)
        deadlineField.setFocusPolicy(Qt.ClickFocus)
        return deadlineField

    def createDeleteTaskButton(self, buttonName):
        button = QPushButton('Delete')
        button.setObjectName(buttonName)
        self.setDefaultFontForWidget(button)
        button.setMaximumHeight(100)
        button.setMaximumWidth(150)
        button.clicked.connect(self.deleteCurrentTask)
        return button

    def saveCurrentTask(self):
        sender = self.sender()
        id = sender.objectName()
        oldTask = getOne(id)
        name = self.currentTitle.text()
        description = self.currentDescription.toPlainText()
        deadline = self.currentDeadline.text()
        isurgent = self.currentIsUrgent.currentText()
        oldTask.updateTask(name, description, deadline, isurgent)
        self.refreshWindow()

    def deleteCurrentTask(self):
        sender = self.sender()
        id = sender.objectName()
        currentTask = getOne(id)
        self.detailsWindow.close()
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
        self.tabs = self.createTabs()
        if firstIndex == 1:
            self.tabs.setCurrentIndex(1)
            self.checkYourTasks.setCurrentIndex(secondIndex)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
