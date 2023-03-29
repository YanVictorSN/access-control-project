from __future__ import annotations

import os
import pathlib
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from run_subprocess import run_subprocess


CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
UI_PATH = pathlib.Path(CURRENT_FILE_PATH, 'ui', 'training.ui')
EXAMPLE = pathlib.Path(CURRENT_FILE_PATH, 'main.py')


class TemplateWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi(UI_PATH, self)
        self.button_clicked_event()
        self.show()

    def button_clicked_event(self):
        self.example_qPB.clicked.connect(self.go_to_example)
        self.close_qPB.clicked.connect(self.close)

    def go_to_example(self):
        run_subprocess(EXAMPLE)


if __name__ == '__main__':
    App = QApplication([])
    Home = TemplateWindow()
    sys.exit(App.exec())
