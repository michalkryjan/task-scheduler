from PyQt5.QtWidgets import QStatusBar


class StatusBar(QStatusBar):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('padding-bottom: 12px; font-size: 16px;')

    def msgTaskAdded(self):
        self.showMessage('Successfully added!', 3000)

    def msgTaskDone(self):
        self.showMessage('Good job with finishing the task!', 3000)

    def msgTaskDeleted(self):
        self.showMessage('Task deleted!', 3000)

    def msgTaskUpdated(self):
        self.showMessage('Task details updated!', 3000)
