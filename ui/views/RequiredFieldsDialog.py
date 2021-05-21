from PyQt5.QtCore import QObject, pyqtSignal, Qt
from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QHBoxLayout, QPushButton, QKeySequenceEdit, QSpacerItem, QDialog
from ..Defaults import *
from .SettingsAdditionalMenuView import SettingsAdditionalMenuView


class RequirementsDialog(QDialog):
    def __init__(self, email, password):
        super().__init__()
        if email == '':
            self.createEmailRequirement()
        if password == '':
            self.createPasswordRequirement()

    def createEmailRequirement(self):
        pass

    def createPasswordRequirement(self):
        pass
