from __future__ import annotations

import json
import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QWidget

from run_subprocess import run_subprocess


CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
UI = os.path.join(CURRENT_FILE_PATH, 'ui', 'course.ui')
COURSE_STUDENT_LIST = os.path.join(CURRENT_FILE_PATH, 'course_student_list.py')
COURSE_ATTENDANCE_LIST = os.path.join(CURRENT_FILE_PATH, 'course_attendance_list.py')
COURSE_DB = os.path.join(CURRENT_FILE_PATH, 'database', 'Course.json')


class CourseWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi(UI, self)
        self.init_ui()
        self.button_clicked_event()
        self.course_DB = self.get_database(COURSE_DB)
        self.set_classes_info()
        self.show()

    def init_ui(self):
        self.course_qTW.setHorizontalHeaderLabels(['Código', 'Ano', 'Alunos', 'Turma'])
        self.course_qTW.resizeColumnsToContents()

    def button_clicked_event(self):
        self.manage_attendance_qPB.clicked.connect(self.go_to_course_attendance_list)
        self.manage_students_qPB.clicked.connect(self.go_to_course_student_list)
        self.close_qPB.clicked.connect(self.close)

    def get_database(self, path):
        with open(path, encoding='utf-8') as f:
            return json.load(f)

    def set_classes_info(self):
        data_classes = self.course_DB['courses']
        self.course_qTW.setRowCount(len(data_classes))

        for i, courses in enumerate(data_classes):
            course_code = QTableWidgetItem(courses['course_code'])
            course_year = QTableWidgetItem(str(courses['course_year']))
            course_students = QTableWidgetItem(str(i + 10))
            course_name = QTableWidgetItem(courses['course_name'])
            self.course_qTW.setItem(i, 0, course_code)
            self.course_qTW.setItem(i, 1, course_year)
            self.course_qTW.setItem(i, 2, course_students)
            self.course_qTW.setItem(i, 3, course_name)

    def go_to_course_attendance_list(self):
        run_subprocess(COURSE_ATTENDANCE_LIST)

    def go_to_course_student_list(self):
        run_subprocess(COURSE_STUDENT_LIST)


if __name__ == '__main__':
    App = QApplication(sys.argv)
    Home = CourseWindow()
    Home.show()
    App.exec_()
