from __future__ import annotations

import json
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QWidget

from ui.ui_course_student_list import Ui_StudentList_qW

CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
STUDENT_DB = os.path.join(CURRENT_FILE_PATH, 'database', 'Student.json')
COURSE_DB = os.path.join(CURRENT_FILE_PATH, 'database', 'Course.json')


class CourseStudentListWindow(QWidget, Ui_StudentList_qW):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.init_ui()
        self.button_clicked_event()
        self.student_DB = self.get_database(STUDENT_DB)
        self.course_DB = self.get_database(COURSE_DB)
        self.data = None
        self.show()

    def init_ui(self):
        self.student_qTW.setHorizontalHeaderLabels(['Matrícula', 'Nome'])
        self.student_qTW.resizeColumnsToContents()
    
    def receive_data(self, data):
        data_courses = self.course_DB["courses"]
        for i in data_courses:
            class_id = i["course_id"]
            if class_id == int(data):
                self.data = class_id
                course_name = i["course_name"]
                course_year = i["course_year"]
                name_and_year = f"{course_name} {course_year}"
                self.course_name_qL.setText(f"Turma: {name_and_year}")
                self.show_students_from_database()
                break

    def button_clicked_event(self):
        self.add_student_qPB.clicked.connect(self.add_student_to_ui)
        self.remove_student_qPB.clicked.connect(self.remove_student_from_ui)
        self.student_qTW.itemSelectionChanged.connect(self.load_student_data)
        self.close_qPB.clicked.connect(self.close)

    def get_database(self, path):
        with open(path, encoding='utf-8') as f:
            return json.load(f)

    def set_database(self, data):
        with open(STUDENT_DB, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

    def show_students_from_database(self):
        count = 0
        for student in self.student_DB['students']:
            if student["student_course_id"] == str(self.data):
                self.insert_student_to_ui(count, student['student_code'], student['student_name'])
                count += 1

    def add_student_to_database(self, code, name):
        student_id = len(self.student_DB['students']) + 1
        student_data = {
            'student_id': int(student_id),
            'student_code': str(code),
            'student_name': str(name),
            'student_course_id':str(self.data)
        }
        self.student_DB['students'].append(student_data)
        self.set_database(self.student_DB)

    def edit_student_to_database(self, code, name):
        for student in self.student_DB['students']:
            if student['student_code'] == code:
                student['student_name'] = str(name)
                self.set_database(self.student_DB)
                break

    def remove_student_from_database(self, name):
        students = self.student_DB['students']
        index_to_delete = next((index for (index, student) in enumerate(
            students) if student['student_name'] == name), None)
        if index_to_delete is not None:
            students.remove(students[index_to_delete])
            self.set_database(self.student_DB)

    def add_student_to_ui(self):
        code = self.student_code_qLE.text()
        name = self.student_name_qLE.text()

        if not self.is_valid_input(code, name):
            return

        row_position, existing_row = self.find_student_row(code)
        if existing_row is not None:
            self.student_qTW.setItem(existing_row, 1, QTableWidgetItem(name))
            self.edit_student_to_database(code, name)
            self.message_qLB.setText('Editado com sucesso')
        else:
            self.insert_student_to_ui(row_position, code, name)
            self.add_student_to_database(code, name)
            self.message_qLB.setText('Adicionado com sucesso')

        self.clear_input_fields()
        self.student_code_qLE.setDisabled(False)

    def remove_student_from_ui(self):
        selected_items = self.student_qTW.selectedItems()

        if not selected_items:
            self.message_qLB.setText('Selecione um estudante')
            return

        name = self.student_name_qLE.text()
        self.remove_student_from_database(name)
        row = selected_items[0].row()
        self.student_qTW.removeRow(row)
        self.message_qLB.setText('Removido com sucesso')

    def is_valid_input(self, code, name):
        self.student_code_qLE.setStyleSheet('')
        self.student_name_qLE.setStyleSheet('')

        if not code or not name:
            self.message_qLB.setText('Preencha os campos')
            if not code:
                self.student_code_qLE.setStyleSheet('border: 1px solid red;')
            if not name:
                self.student_name_qLE.setStyleSheet('border: 1px solid red;')
            return False

        return True

    def insert_student_to_ui(self, row_position, code, name):
        self.student_qTW.insertRow(row_position)
        self.student_qTW.setItem(row_position, 0, QTableWidgetItem(code))
        self.student_qTW.setItem(row_position, 1, QTableWidgetItem(name))

    def clear_input_fields(self):
        self.student_code_qLE.clear()
        self.student_name_qLE.clear()
        self.student_code_qLE.setStyleSheet('')
        self.student_name_qLE.setStyleSheet('')

    def find_student_row(self, code):
        row_position = self.student_qTW.rowCount()
        existing_row = next(
            (
                row
                for row in range(row_position)
                if self.student_qTW.item(row, 0).text() == code
            ),
            None,
        )
        return row_position, existing_row

    def load_student_data(self):
        selected_items = self.student_qTW.selectedItems()
        if not selected_items:
            return
        row = selected_items[0].row()
        self.student_code_qLE.setText(self.student_qTW.item(row, 0).text())
        self.student_name_qLE.setText(self.student_qTW.item(row, 1).text())
        self.student_code_qLE.setDisabled(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.student_qTW.rect().contains(event.pos()):
            self.student_qTW.clearSelection()
            self.student_code_qLE.setDisabled(False)


if __name__ == '__main__':
    App = QApplication([])
    Home = CourseStudentListWindow()
    Home.show()
    sys.exit(App.exec())
