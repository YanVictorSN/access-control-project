from __future__ import annotations

import os
import pathlib
import sys
import json
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QObject, pyqtSignal
from course_student_list import CourseStudentListWindow
from course_attendance_list import CourseAttendanceListWindow
from PyQt5.QtWidgets import QApplication, QMessageBox


CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
UI_PATH = pathlib.Path(CURRENT_FILE_PATH, 'ui', 'course.ui')
COURSE_STUDENT_LIST = pathlib.Path(CURRENT_FILE_PATH, 'course_student_list.py')
COURSE_ATTENDANCE_LIST = pathlib.Path(CURRENT_FILE_PATH, 'course_attendance_list.py')
DATABASE_PATH = pathlib.Path(CURRENT_FILE_PATH, 'database', 'student_data.JSON')

class CourseWindow(QWidget):
    my_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi(UI_PATH, self)
        self.init_ui()
        self.button_clicked_event()
        self.get_dataset(DATABASE_PATH)
        self.set_classes_info()
        

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
        self.emit_signal_to_attendance_list()
        # run_subprocess(COURSE_ATTENDANCE_LIST)

    def go_to_course_student_list(self):
        self.emit_signal_to_student_list()
        # run_subprocess(COURSE_STUDENT_LIST)

    def emit_signal_to_attendance_list(self):
        Attendance = CourseAttendanceListWindow()
        AttendanceData = Attendance.receive_data
        self.my_signal.connect(AttendanceData)
        self.send_data()
      
    def emit_signal_to_student_list(self):
        selected_items = self.course_qTW.selectedItems()
        if selected_items:
            Course = CourseStudentListWindow()
            CourseData = Course.receive_data
            self.my_signal.connect(CourseData)
            self.send_data()
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Por favor, selecione um turma.")
            msgBox.setWindowTitle("Mensagem de informação")
            msgBox.exec_()

    def send_data(self):
        selected_items = self.course_qTW.selectedItems()
        if selected_items:
            selected_class_code = selected_items[3].text()

            data_classes = self.database["classes"]
            for i in data_classes:  
                class_name = i["class_name"]
                if class_name == selected_class_code:
                    class_id = i["class_id"]
                    self.my_signal.emit(str(class_id))


if __name__ == '__main__':
    App = QApplication(sys.argv)
    Home = CourseWindow()
    Home.show()
    App.exec_()
