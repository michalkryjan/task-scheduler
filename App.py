from PyQt5.QtWidgets import qApp, QMainWindow, QApplication, QWidget, QFormLayout, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QDateEdit, QComboBox, QPushButton, QTabWidget, QScrollArea, QGroupBox, QDialog
from PyQt5.QtCore import Qt, QDate, QDateTime, QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap
import sys, os
from dbActions import addTaskToDb, startDb
from Task import Task
from datetime import date, datetime
from Layouts import *


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        startDb()
        mainWidget = QWidget()
        mainWidget.setLayout(TabWidgetLayout())
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