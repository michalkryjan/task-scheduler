from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from views.NewTaskView import NewTaskView
from views.TaskListView import TaskListView
from database.GetTasks import *


class TabWidget(QWidget):
    def __init__(self, statusBar):
        super().__init__()
        self.statusBar = statusBar
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
        newTaskView = NewTaskView(self.statusBar, self.refresh)
        widget.setLayout(newTaskView)
        return widget

    def InitCheckYourTasksTabs(self, parentTab):
        allToDoTabView = TaskListView(getAllTasks(), self.statusBar, self.refresh)
        forTodayTabView = TaskListView(getForTodayTasks(), self.statusBar, self.refresh)
        forTomorrowTabView = TaskListView(getForTomorrowTasks(), self.statusBar, self.refresh)
        urgentTabView = TaskListView(getUrgentTasks(), self.statusBar, self.refresh)
        notUrgentTabView = TaskListView(getNotUrgentTasks(), self.statusBar, self.refresh)
        doneTabView = TaskListView(getDoneTasks(), self.statusBar, self.refresh)
        self.createTabWithViewUnder(parentTab, 'All to do', allToDoTabView)
        self.createTabWithViewUnder(parentTab, 'For today', forTodayTabView)
        self.createTabWithViewUnder(parentTab, 'For tomorrow', forTomorrowTabView)
        self.createTabWithViewUnder(parentTab, 'Urgent', urgentTabView)
        self.createTabWithViewUnder(parentTab, 'Not urgent', notUrgentTabView)
        self.createTabWithViewUnder(parentTab, 'Done', doneTabView)

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
