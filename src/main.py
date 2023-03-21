from __future__ import annotations

import subprocess
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi('ui/main.ui', self)
        self.training_QPB.clicked.connect(self.goToTraining)
        self.close_QPB.clicked.connect(self.close)
        self.show()

    def goToTraining(self):
        subprocess.Popen(['python', 'training.py'])


if __name__ == '__main__':
    App = QApplication(sys.argv)
    Home = MainWindow()
    sys.exit(App.exec())
