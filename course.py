from __future__ import annotations

import json
import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QObject, pyqtSignal
from course_student_list import CourseStudentListWindow
from course_attendance_list import CourseAttendanceListWindow
from PyQt5.QtWidgets import QApplication, QMessageBox


CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
UI = os.path.join(CURRENT_FILE_PATH, 'ui', 'course.ui')
COURSE_STUDENT_LIST = os.path.join(CURRENT_FILE_PATH, 'course_student_list.py')
COURSE_ATTENDANCE_LIST = os.path.join(CURRENT_FILE_PATH, 'course_attendance_list.py')
COURSE_DB = os.path.join(CURRENT_FILE_PATH, 'database', 'Course.json')


class CourseWindow(QWidget):
    my_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi(UI, self)
        self.init_ui()
        self.button_clicked_event()
        self.course_DB = self.get_database(COURSE_DB)
        self.set_classes_info()

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
        self.emit_signal_to_attendance_list()

    def go_to_course_student_list(self):
        self.emit_signal_to_student_list()

    def emit_signal_to_attendance_list(self):
        selected_items = self.course_qTW.selectedItems()
        if selected_items:
            self.Attendance = CourseAttendanceListWindow()
            self.AttendanceData = self.Attendance.receive_data
            self.my_signal.connect(self.AttendanceData)
            self.send_data()
        else:
            self.send_message_error()

    def emit_signal_to_student_list(self):
        selected_items = self.course_qTW.selectedItems()
        if selected_items:
            self.Course = CourseStudentListWindow()
            self.CourseData = self.Course.receive_data
            self.my_signal.connect(self.CourseData)
            self.send_data()
        else:
            self.send_message_error()

    def send_message_error(self):
        self.msgBox = QMessageBox()
        self.msgBox.setIcon(QMessageBox.Information)
        self.msgBox.setText("Por favor, selecione um turma.")
        self.msgBox.setWindowTitle("Mensagem de informação")
        self.msgBox.exec_()

    def send_data(self):
        selected_items = self.course_qTW.selectedItems()
        selected_course_code = selected_items[3].text()
        data_courses = self.course_DB["courses"]
        for i in data_courses:
            course_name = i["course_name"]
            if course_name == selected_course_code:
                course_id = i["course_id"]
                self.my_signal.emit(str(course_id))


if __name__ == '__main__':
    App = QApplication(sys.argv)
    Home = CourseWindow()
    Home.show()
    App.exec_()
