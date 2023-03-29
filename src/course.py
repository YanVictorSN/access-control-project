from __future__ import annotations

import os
import pathlib
import sys
import json
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QWidget
from run_subprocess import run_subprocess


CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
UI_PATH = pathlib.Path(CURRENT_FILE_PATH, 'ui', 'course.ui')
COURSE_STUDENT_LIST = pathlib.Path(CURRENT_FILE_PATH, 'course_student_list.py')
COURSE_ATTENDANCE_LIST = pathlib.Path(CURRENT_FILE_PATH, 'course_attendance_list.py')
DATABASE_PATH = pathlib.Path(CURRENT_FILE_PATH, 'database', 'student_data.JSON')


class CourseWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi(UI_PATH, self)
        self.init_ui()
        self.button_clicked_event()
        self.get_dataset(DATABASE_PATH)
        self.set_classes_info()
        self.show()

    def init_ui(self):
        self.course_qTW.setHorizontalHeaderLabels(['Código', 'Ano', 'Alunos', 'Turma'])
        self.course_qTW.resizeColumnsToContents()

    def button_clicked_event(self):
        self.manage_attendance_qPB.clicked.connect(self.go_to_course_attendance_list)
        self.manage_students_qPB.clicked.connect(self.go_to_course_student_list)
        self.close_qPB.clicked.connect(self.close)

    def get_dataset(self, path):
        with open(path, encoding='utf-8') as f:
            self.database = json.load(f)
            return self.database

    def set_classes_info(self):
        data_classes = self.database["classes"]
        self.course_qTW.setRowCount(len(data_classes))

        for i, classes in enumerate(data_classes):
            class_code = QTableWidgetItem(classes["class_code"])
            class_year = QTableWidgetItem(str(classes["class_year"]))
            total_students = QTableWidgetItem(str(classes["number_of_students"]))
            class_name = QTableWidgetItem(classes["class_name"])
            self.course_qTW.setItem(i, 0,  class_code)
            self.course_qTW.setItem(i, 1,  class_year)
            self.course_qTW.setItem(i, 2,  total_students)
            self.course_qTW.setItem(i, 3,  class_name)

    def go_to_course_attendance_list(self):
        run_subprocess(COURSE_ATTENDANCE_LIST)

    def go_to_course_student_list(self):
        run_subprocess(COURSE_STUDENT_LIST)


if __name__ == '__main__':
    App = QApplication(sys.argv)
    Home = CourseWindow()
    Home.show()
    App.exec_()
