from configparser import ConfigParser
import pathlib
import os
import winshell
import sys
from shutil import rmtree


def getSpecialKeys():
    specials = {"N0": 96, "N1": 97, "N2": 98, "N3": 99, "N4": 100, "N5": 101, "N6": 102, "N7": 103, "N8": 104,
                   "N9": 105, "Ndel": 110, "Pup": 2081, "Pdown": 2082, "Home": 2084, "End": 2083, "Insert": 2093,
                   "Numlock": 2192, "Capslock": 20, "Space": 32, "Shift": 256, "Ctrl": 512, "Alt": 1024, "Delete": 127,
                   "Up": 2086, "Down": 2088, "Left": 2085, "Right": 2087}
    return specials


def keySequenceToOrd(sequence):
    specials = getSpecialKeys()
    keysSplitted = sequence.split('+')
    result = ''
    for i in range(0, len(keysSplitted)):
        if keysSplitted[i] in specials.keys():
            for key, code in specials.items():
                if key == keysSplitted[i]:
                    result += str(code)
        else:
            result += str(ord(keysSplitted[i]))
        if i < len(keysSplitted) - 1:
            result += '+'
    return result


def createKeyShortcuts():
    rootPath = pathlib.PureWindowsPath(os.path.abspath(__file__)).parents[1]
    config = ConfigParser()
    config.read(os.path.join(rootPath, 'config.ini'))
    if config.get('shortcut_keys', 'is_active') == 'yes':
        shortcutsPath = os.path.join(rootPath, 'settings/shortcuts')
        if os.path.exists(shortcutsPath):
            rmtree('shortcuts')
        os.mkdir('shortcuts')
        i = 1
        while config.has_option('shortcut_keys', f'shortcut_key_{i}'):
            keySequence = keySequenceToOrd(config.get('shortcut_keys', f'shortcut_key_{i}'))
            linkPath = os.path.join(shortcutsPath, f'shortcut_{i}.lnk')
            with winshell.shortcut(linkPath) as link:
                link.path = sys.executable
                link.description = f'shortcut_{i}'
                link.arguments = "-m winshell"
                link.hotkey = eval(keySequence)
            i += 1
