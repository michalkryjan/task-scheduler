from PyQt5.QtWidgets import qApp, QWidget, QFormLayout, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QDateEdit, QComboBox, QPushButton, QTabWidget, QScrollArea, QDialog
from PyQt5.QtCore import Qt, QDate, QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap
from Task import Task
from GetTasks import GetTasks
from datetime import date, datetime
from dbActions import addTaskToDb


class Fonts(object):
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


class TabWidget(QWidget, Fonts, GetTasks):
    def __init__(self): 
        super().__init__()
        self.mainLayout = QVBoxLayout()
        self.createTabWidget()
        self.setLayout(self.mainLayout)

    def createTabWidget(self):
        self.tabWidget = QTabWidget()
        self.setFontForTabs(self.tabWidget)
        self.InitMainTabs(self.tabWidget)
        self.InitCheckYourTasksTabs(self.checkYourTasks)
        self.mainLayout.addWidget(self.tabWidget)

    def setFontForTabs(self, tabs):
        font = QFont()
        font.setFamily('Century Gothic')
        font.setPointSize(9)
        tabs.setFont(font)

    def InitMainTabs(self, tabWidget):
        self.checkYourTasks = QTabWidget()
        tabWidget.addTab(self.InitNewTaskView(), 'New task')
        tabWidget.addTab(self.checkYourTasks, 'Check your tasks')

    def InitNewTaskView(self):
        widget = QWidget()
        newTaskView = NewTaskView(self.refresh)
        widget.setLayout(newTaskView)
        return widget

    def InitCheckYourTasksTabs(self, parentTab):
        self.createTabWithViewUnder(parentTab, 'All to do', TaskListView(self.getAllTasks(), self.refresh))
        self.createTabWithViewUnder(parentTab, 'For today', TaskListView(self.getForTodayTasks(), self.refresh))
        self.createTabWithViewUnder(parentTab, 'For tomorrow', TaskListView(self.getForTomorrowTasks(), self.refresh))
        self.createTabWithViewUnder(parentTab, 'Urgent', TaskListView(self.getUrgentTasks(), self.refresh))
        self.createTabWithViewUnder(parentTab, 'Not urgent', TaskListView(self.getNotUrgentTasks(), self.refresh))
        self.createTabWithViewUnder(parentTab, 'Done', TaskListView(self.getDoneTasks(), self.refresh))

    def createTabWithViewUnder(self, parentTab, name, taskListLayout):
        widget = QWidget()
        widget.setLayout(taskListLayout)
        parentTab.addTab(widget, name)

    def refresh(self):
        firstIndex = self.tabWidget.currentIndex()
        if firstIndex == 1:
            secondIndex = self.checkYourTasks.currentIndex()
        for i in reversed(range(self.mainLayout.count())): 
            self.mainLayout.itemAt(i).widget().setParent(None)
        self.createTabWidget()
        if firstIndex == 1:
            self.tabWidget.setCurrentIndex(1)
            self.checkYourTasks.setCurrentIndex(secondIndex)


class TaskListView(QVBoxLayout, Fonts, GetTasks):
    def __init__(self, tasks, refreshMethod):
        super().__init__() 
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
        detailsWindow = self.createDetailsWindow()
        sender = self.sender()
        selectedTask = self.selectOneTask(sender.objectName())
        selectedTaskView = SelectedTaskView(detailsWindow, selectedTask, self.refreshWindow)
        detailsWindow.setLayout(selectedTaskView)
        detailsWindow.exec_()

    def createDetailsWindow(self):
        window =  QDialog()
        window.setWindowIcon(QIcon('icons/calendar_icon.png'))
        window.resize(800,700)
        window.setWindowTitle('Details')
        window.setWindowModality(Qt.ApplicationModal)
        return window

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
        task = self.selectOneTask(sender.objectName())
        task.setTaskAsDone()
        self.refreshWindow()


class DefaultOneTaskView(QVBoxLayout, Fonts):
    def __init__(self):
        super().__init__() 
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


class NewTaskView(DefaultOneTaskView):
    def __init__(self, refreshMethod):
        super().__init__() 
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
        isurgent = self.isurgent.currentText()
        addTaskToDb(title, description, deadline, isurgent)
        self.refreshWindow()


class SelectedTaskView(DefaultOneTaskView):
    def __init__(self, QDialogWindow, selectedTask, refreshMethod):
        super().__init__() 
        self.refreshWindow = refreshMethod
        self.selectedTask = selectedTask
        self.QDialogWindow = QDialogWindow
        self.mainLabel.setText('Edit task')
        self.setCurrentDataForFields()
        self.deleteButton = self.createDeleteButton(self.footerLayout)
        self.setMethodsForButtons()

    def createDeleteButton(self, layout):
        button = QPushButton('Delete')
        button.setObjectName(str(self.selectedTask.id))
        self.setDefaultFontForWidget(button)
        button.setMaximumHeight(100)
        button.setMaximumWidth(150)
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

    def deleteTask(self):
        self.selectedTask.deleteTask()
        self.refreshWindow()
        self.QDialogWindow.close()

    def setCurrentDataForFields(self):
        self.title.setText(self.selectedTask.name)
        self.description.setText(self.selectedTask.description)
        self.isurgent.setCurrentText(self.selectedTask.is_urgent)
        d, m, y = map(int, self.selectedTask.deadline.split('.'))
        self.deadline.setDate(QDate(y, m, d))
