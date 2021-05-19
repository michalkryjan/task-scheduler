from PyQt5.QtWidgets import QLabel
from .Fonts import *

def createDefaultOneLineLabel(content):
    label = QLabel(content)
    setDefaultFontForSettings(label)
    return label


def createDefaultMultiLineLabel(content):
    label = QLabel(content)
    setDefaultFontForSettings(label)
    label.setWordWrap(True)
    return label


def setMaxSizeForWidget(widget, height, width):
    widget.setMaximumHeight(height)
    widget.setMaximumWidth(width)


def setMinSizeForWidget(widget, height, width):
    widget.setMinimumHeight(height)
    widget.setMinimumWidth(width)
