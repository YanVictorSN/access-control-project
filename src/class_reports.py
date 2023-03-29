from __future__ import annotations

import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from run_subprocess import run_subprocess

CURRENT_FILE_PATH = os.path.abspath(__file__)
UI_PATH = os.path.join(os.path.dirname(CURRENT_FILE_PATH), 'ui', 'class_reports.ui')
ATTENDACE_LIST = os.path.join(os.path.dirname(CURRENT_FILE_PATH), 'course_attendance_list.py')
TRAINING = os.path.join(os.path.dirname(CURRENT_FILE_PATH), 'training.py')

class ClassReportsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi(UI_PATH, self)
        self.init_ui()
        self.button_clicked_event()
        self.show()

    def init_ui(self):
        self.course_qTW.setHorizontalHeaderLabels(['Código', 'Status', 'Alunos'])
        self.course_qTW.resizeColumnsToContents()

    def button_clicked_event(self):
        self.btn_back.clicked.connect(self.go_to_course_attendance_list)
        self.btn_training.clicked.connect(self.go_to_training)

    def go_to_course_attendance_list(self):
        run_subprocess(ATTENDACE_LIST)

    def go_to_training(self):
        run_subprocess(TRAINING)

if __name__ == '__main__':
    App = QApplication(sys.argv)
    Home = ClassReportsWindow()
    Home.show()
    App.exec_()
