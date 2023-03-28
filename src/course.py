from __future__ import annotations

import os
import pathlib
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from run_subprocess import run_subprocess


CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
UI_PATH = pathlib.Path(CURRENT_FILE_PATH, 'ui', 'course.ui')
COURSE_STUDENT_LIST = pathlib.Path(CURRENT_FILE_PATH, 'course_student_list.py')
COURSE_ATTENDANCE_LIST = pathlib.Path(CURRENT_FILE_PATH, 'course_attendance_list.py')


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
        self.manage_attendance_qPB.clicked.connect(self.go_to_course_attendance_list)
        self.manage_students_qPB.clicked.connect(self.go_to_course_student_list)
        self.close_qPB.clicked.connect(self.close)

    def go_to_course_attendance_list(self):
        run_subprocess(COURSE_ATTENDANCE_LIST)

    def go_to_course_student_list(self):
        run_subprocess(COURSE_STUDENT_LIST)


if __name__ == '__main__':
    App = QApplication(sys.argv)
    Home = CourseWindow()
    Home.show()
    App.exec_()
