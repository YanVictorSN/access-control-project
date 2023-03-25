from __future__ import annotations
from run_subprocess import run_subprocess

import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget


CURRENT_FILE_PATH = os.path.abspath(__file__)
UI_PATH = os.path.join(os.path.dirname(CURRENT_FILE_PATH), 'ui', 'course.ui')
STUDENT = os.path.join(os.path.dirname(
    CURRENT_FILE_PATH), 'course_student_list.py')


class CourseWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi(UI_PATH, self)
        self.init_ui()
        self.button_clicked_event()
        self.show()

    def init_ui(self):
        print(self)
        self.course_qTW.setHorizontalHeaderLabels(
            ['Código', 'Ano', 'Alunos', 'Turma'])
        self.course_qTW.resizeColumnsToContents()

    def button_clicked_event(self):
        self.close_qPB.clicked.connect(self.close)
        self.manage_students_qPB.clicked.connect(self.go_to_student_list)

    def go_to_student_list(self):
        print('ok')
        run_subprocess(STUDENT)


if __name__ == '__main__':
    App = QApplication(sys.argv)
    Home = CourseWindow()
    Home.show()
    App.exec_()
