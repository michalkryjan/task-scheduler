from PyQt5.QtWidgets import qApp, QMainWindow, QApplication, QWidget, QFormLayout, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QDateEdit, QComboBox, QPushButton, QTabWidget, QScrollArea, QGroupBox
from PyQt5.QtCore import Qt, QDate, QDateTime
from PyQt5.QtGui import QFont
import sys
from db_actions import addTaskToDb
from task import Task, GetTasks


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Task scheduler')
        self.tab_widget = TabWidget(self)
        self.setCentralWidget(self.tab_widget)
        self.resize(800, 700)
        self.setMaximumHeight(700)
        self.setMaximumWidth(800)
        self.show()


class TabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)   
        self.layout = QVBoxLayout(self)
        self.getTasks = GetTasks()
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
        # add tabs
        self.tabs.addTab(self.newTask, 'New Task')
        self.tabs.addTab(self.checkYourTasks, 'Check your tasks')
        self.checkYourTasks.addTab(self.allTasks, 'All')
        self.checkYourTasks.addTab(self.forTodayTasks, 'For today')
        self.checkYourTasks.addTab(self.forTomorrowTasks, 'For tomorrow')
        self.checkYourTasks.addTab(self.urgentTasks, 'Urgent')
        self.checkYourTasks.addTab(self.notUrgentTasks, 'Not urgent')
        # creating views for tabs
        self.newTaskView()
        self.allTasksView()
        self.forTodayTasksView()
        self.forTomorrowTasksView()
        self.urgentTasksView()
        self.notUrgentTasksView()
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
        self.newTask.outerLayout.addWidget(self.newtask_label, alignment=Qt.AlignCenter, )
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
        self.save.clicked.connect(self.saveTask)
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

    def allTasksView(self):
        groupboxLayout = QVBoxLayout()
        tasks = self.getTasks.all()
        for task in tasks:
            row = QHBoxLayout()
            # task name
            name = QLabel(task.name)
            name.setMaximumHeight(60)
            name.setMaximumWidth(400)
            name.setMinimumWidth(400)
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
            taskDone = QPushButton('Done')
            taskDone.setMaximumWidth(46)
            taskDone.setObjectName(str(task.id))
            taskDone.clicked.connect(self.setAsDone)
            row.addWidget(taskDone)
            # add task to the list
            groupboxLayout.addLayout(row)
        # add scroll for the list
        groupbox = QGroupBox()
        groupbox.setLayout(groupboxLayout)
        scroll = QScrollArea()
        scroll.setWidget(groupbox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(600)
        scroll.setMaximumWidth(780)
        # connecting layouts
        self.allTasks.layout = QVBoxLayout()
        self.allTasks.layout.addWidget(scroll)
        self.allTasks.setLayout(self.allTasks.layout)
    
    def forTodayTasksView(self):
        pass
    
    def forTomorrowTasksView(self):
        pass
    
    def urgentTasksView(self):
        pass

    def notUrgentTasksView(self):
        pass

    # events for buttons
    def saveTask(self):
        name = self.title.text()
        description = self.description.toPlainText()
        deadline = self.deadline.text()
        is_urgent = self.isurgent.currentText()
        addTaskToDb(name, description, deadline, is_urgent)

    def checkDetails(self):
        sender = self.sender()
        id = sender.objectName()
        # open new window for editing task here
        print(id + ' was pressed (check details)') # signal test

    def setAsDone(self):
        sender = self.sender()
        task = self.getTasks.one(sender.objectName())
        task.setTaskAsDone()
        print(id + ' was pressed (set as done)') # signal test


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
