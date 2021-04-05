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
        mainLayout.addWidget(self.createNewTaskMainLabel(), alignment=Qt.AlignCenter)
        mainLayout.addLayout(self.createTaskBodyLayout())
        mainLayout.addLayout(self.createTaskFooterLayout())
        newTask.setLayout(mainLayout)

    def createTaskBodyLayout(self):
        self.title = self.createTitleField()
        self.description = self.createDescriptionField()
        self.deadline = self.createDeadlineField()
        self.isurgent = self.createIsUrgentField()
        bodyLayout = QFormLayout()
        bodyLayout.addRow(self.createTitleLabel(), self.title)
        bodyLayout.addRow(self.createDescriptionLabel(), self.description)
        bodyLayout.addRow(self.createDeadlineLabel(), self.deadline)
        bodyLayout.addRow(self.createIsUrgentLabel(), self.isurgent)
        return bodyLayout

    def createTaskFooterLayout(self):
        self.save = self.createSaveButton()
        self.close = self.createCloseButton()
        footerLayout = QHBoxLayout()
        footerLayout.addWidget(self.save)
        footerLayout.addWidget(self.close)
        return footerLayout

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

    def createNewTaskMainLabel(self):
        label = QLabel('Add a new task')
        self.setBiggerFontForWidget(label)
        return label

    def createTitleLabel(self):
        label = QLabel('Title:')
        self.setDefaultFontForWidget(label)
        return label

    def createTitleField(self):
        title = QLineEdit()
        title.setMaxLength(100)
        title.setMaximumWidth(640)
        self.setDefaultFontForWidget(title)
        return title

    def createDescriptionLabel(self):
        label = QLabel('Description:')
        self.setDefaultFontForWidget(label)
        return label
    
    def createDescriptionField(self):
        description = QTextEdit()
        self.setDefaultFontForWidget(description)
        description.setMaximumHeight(200)
        description.setMaximumWidth(640)
        return description

    def createDeadlineLabel(self):
        label = QLabel('Deadline:')
        self.setDefaultFontForWidget(label)
        return label

    def createDeadlineField(self):
        deadline = QDateEdit()
        self.setDefaultFontForWidget(deadline)
        deadline.setMaximumHeight(40)
        deadline.setMaximumWidth(130)
        deadline.setDateTime(QDateTime.currentDateTime())
        deadline.setMaximumDate(QDate(2100, 12, 28))
        deadline.setCalendarPopup(True)
        deadline.setFocusPolicy(Qt.ClickFocus)
        return deadline

    def createIsUrgentLabel(self):
        label = QLabel('Is urgent?')
        self.setDefaultFontForWidget(label)
        return label

    def createIsUrgentField(self):
        isurgent = QComboBox()
        self.setDefaultFontForWidget(isurgent)
        isurgent.setMaximumHeight(40)
        isurgent.setMaximumWidth(130)
        isurgent.addItem('Yes')
        isurgent.addItem('No')
        return isurgent

    def createSaveButton(self):
        save = QPushButton('Save')
        self.setDefaultFontForWidget(save)
        save.setMaximumHeight(100)
        save.setMaximumWidth(150)
        save.clicked.connect(self.saveNewTask)
        return save

    def createCloseButton(self):
        close = QPushButton('Close')
        self.setDefaultFontForWidget(close)
        close.setMaximumHeight(100)
        close.setMaximumWidth(150)
        close.clicked.connect(qApp.quit)
        return close

    def saveNewTask(self):
        name = self.title.text()
        description = self.description.toPlainText()
        deadline = self.deadline.text()
        is_urgent = self.isurgent.currentText()
        addTaskToDb(name, description, deadline, is_urgent)
        self.refreshWindow()
        

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

    def createTabView(self, widget, getTasksMethod):
        tasks = getTasksMethod()
        taskList = self.createTaskList(tasks)
        widget.layout = QVBoxLayout()
        widget.layout.addWidget(taskList)
        widget.setLayout(widget.layout)

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
        self.tabs = self.createTabs()
        if firstIndex == 1:
            self.tabs.setCurrentIndex(1)
            self.checkYourTasks.setCurrentIndex(secondIndex)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
