from PyQt5.QtGui import QFont


def setDefaultFontForWidget(widget):
    font = QFont()
    font.setFamily('Sitka Small')
    font.setPointSize(11)
    widget.setFont(font)


def setBiggerFontForWidget(widget):
    font = QFont()
    font.setFamily('Sitka Small')
    font.setPointSize(20)
    widget.setFont(font)


def setDefaultFontForSettings(widget):
    font = QFont()
    font.setFamily('Sitka Display')
    font.setPointSize(9)
    widget.setFont(font)
