#!/usr/bin/python
import debian
import arch
import os, sys
from PySide6 import QtCore, QtWebEngineWidgets, QtGui, QtWidgets

# Constants
SCRIPTDIR = os.path.dirname(os.path.realpath(__file__))
VERSION = 1.0

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(QtCore.QSize(800, 600))
        self.setWindowTitle("Knights and Fights")
        self.setWindowIcon(QtGui.QIcon(":/qt-project.org/styles/commonstyle/images/right-32.png"))
        self.webEngine = QtWebEngineWidgets.QWebEngineView(self)
        self.setCentralWidget(self.webEngine)
    def load(self, file):
        file_url = QtCore.QUrl.fromLocalFile(file)
        self.webEngine.load(QtCore.QUrl(file_url))

def load(container):
    if not os.path.exists("/etc/nspawnbox"):
        os.mkdir("/etc/nspawnbox")
    if container == "arch":
        if not os.path.exists("/etc/podspawn/arch"):
            arch.install_arch()
        os.system("sudo systemd-nspawn -b -D /etc/podspawn/arch --bind=/tmp/.X11-unix -E DISPLAY=:0")
    if container == "debian":
        if not os.path.exists("/etc/podspawn/debian"):
            debian.install_debian()
        os.system("sudo systemd-nspawn -b -D /etc/podspawn/debian --bind=/tmp/.X11-unix -E DISPLAY=:0")

def main():
    app = QtWidgets.QApplication()
    gameWindow = Window()
    gameWindow.show()
    gameWindow.load(f"{SCRIPTDIR}/gui/ui.html")
    app.exec()

main()