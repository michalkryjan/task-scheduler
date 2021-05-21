from PyQt5.QtWidgets import QFormLayout, QDialog
from ..Defaults import *


class RequirementsDialog(QDialog):
    def __init__(self, email, password):
        super().__init__()
        self.setupWindow()
        mainLayout = QFormLayout()
        if email == '':
            mainLayout.addRow(self.createEmailRequirement())
        if password == '':
            mainLayout.addRow(self.createPasswordRequirement())
        self.setLayout(mainLayout)

    def setupWindow(self):
        pass

    def createEmailRequirement(self):
        text = 'You need to pass your email address! (for Gmail account which has enabled option "less secure apps")'
        label = QLabel(text)
        setDefaultFontForSettings(label)
        return label

    def createPasswordRequirement(self):
        text = 'You need to pass your app password! (for app created in your Gmail Account)'
        label = QLabel(text)
        setDefaultFontForSettings(label)
        return label
