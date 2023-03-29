from __future__ import annotations

import os
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget

from run_subprocess import run_subprocess
from ui.ui_template import Ui_Template_qW

CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
MAIN = os.path.join(CURRENT_FILE_PATH, 'main.py')


class TemplateWindow(QWidget, Ui_Template_qW):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.button_clicked_event()
        self.show()

    def button_clicked_event(self):
        self.example_qPB.clicked.connect(self.go_to_example)
        self.close_qPB.clicked.connect(self.close)

    def go_to_example(self):
        run_subprocess(MAIN)


if __name__ == '__main__':
    App = QApplication([])
    Home = TemplateWindow()
    sys.exit(App.exec())
