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
