from __future__ import annotations

import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow


TURMAS = 'ui/classes.ui'
UI_PATH = 'main.py'


class LisTClasses(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi(TURMAS, self)
        self.buttonClickedEvent()
        self.show()

    def buttonClickedEvent(self):
        self.close_QPB.clicked.connect(self.close)


if __name__ == '__main__':
    App = QApplication(sys.argv)
    Home = LisTClasses()
    Home.show()
    App.exec_()
