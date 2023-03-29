from __future__ import annotations

import os
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget

from run_subprocess import run_subprocess
from ui.ui_main import Ui_Main_qW

CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
TRAINING = os.path.join(CURRENT_FILE_PATH, 'training.py')
COURSE = os.path.join(CURRENT_FILE_PATH, 'course.py')


class MainWindow(QWidget, Ui_Main_qW):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.button_clicked_event()
        self.show()

    def button_clicked_event(self):
        self.training_qPB.clicked.connect(self.go_to_training)
        self.attendence_qPB.clicked.connect(self.go_to_course)
        self.close_qPB.clicked.connect(self.close)

    def go_to_training(self):
        run_subprocess(TRAINING)

    def go_to_course(self):
        run_subprocess(COURSE)


if __name__ == '__main__':
    App = QApplication([])
    Home = MainWindow()
    sys.exit(App.exec())
