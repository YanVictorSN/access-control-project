from __future__ import annotations

import subprocess
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget


UI_PATH = 'ui/main.ui'
TRAINING = 'training.py'


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi(UI_PATH, self)
        self.button_clicked_event()
        self.show()

    def button_clicked_event(self):
        self.training_QPB.clicked.connect(self.go_to_training)
        self.close_QPB.clicked.connect(self.close)

    def go_to_training(self):
        subprocess.Popen(['python', TRAINING])


if __name__ == '__main__':
    App = QApplication([])
    Home = MainWindow()
    sys.exit(App.exec())
