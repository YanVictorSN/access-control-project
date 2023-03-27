from __future__ import annotations

import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from run_subprocess import run_subprocess


CURRENT_FILE_PATH = os.path.abspath(__file__)
UI_PATH = os.path.join(os.path.dirname(CURRENT_FILE_PATH), 'ui', 'course.ui')
STUDENT_LIST = os.path.join(os.path.dirname(CURRENT_FILE_PATH), 'course_student_list.py')


class CourseWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi(UI_PATH, self)
        self.init_ui()
        self.button_clicked_event()
        self.show()

    def init_ui(self):
        self.course_qTW.setHorizontalHeaderLabels(['Código', 'Ano', 'Alunos', 'Turma'])
        self.course_qTW.resizeColumnsToContents()

    def button_clicked_event(self):
        self.close_qPB.clicked.connect(self.close)
        self.manage_students_qPB.clicked.connect(self.go_to_student_list)

    def go_to_student_list(self):
        run_subprocess(STUDENT_LIST)


if __name__ == '__main__':
    App = QApplication(sys.argv)
    Home = CourseWindow()
    Home.show()
    App.exec_()
