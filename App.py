from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QIcon
from Layouts import TabWidget, StatusBar
from dbActions import startDb
import sys


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        startDb()
        statusBar = StatusBar()
        self.setStatusBar(statusBar)
        mainWidget = TabWidget(statusBar)
        self.setCentralWidget(mainWidget)
        self.setWindowSize()
        self.setWindowTitle('Task scheduler')
        self.setWindowIcon(QIcon('icons/tasks_icon.png'))
        self.show()

    def setWindowSize(self):
        self.resize(800, 700)
        self.setMaximumHeight(700)
        self.setMaximumWidth(800)
        self.setMinimumWidth(800)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
