from __future__ import annotations

import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from run_subprocess import run_subprocess


CURRENT_FILE_PATH = os.path.abspath(__file__)
UI_PATH = os.path.join(os.path.dirname(CURRENT_FILE_PATH), 'ui', 'main.ui')
TRAINING = os.path.join(os.path.dirname(CURRENT_FILE_PATH), 'training.py')


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi(UI_PATH, self)
        self.button_clicked_event()
        self.show()

    def button_clicked_event(self):
        self.training_qPB.clicked.connect(self.go_to_training)
        self.close_qPB.clicked.connect(self.close)

    def go_to_training(self):
        run_subprocess(TRAINING)


if __name__ == '__main__':
    App = QApplication([])
    Home = MainWindow()
    sys.exit(App.exec())
