from __future__ import annotations

import os
import sys
import json
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QWidget


CURRENT_FILE_PATH = os.path.abspath(__file__)
UI_PATH = os.path.join(os.path.dirname(CURRENT_FILE_PATH), 'ui', 'course_student_list.ui')
DATABASE_PATH = "database/student_data.json"

class CourseStudentListWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi(UI_PATH, self)
        self.init_ui()
        self.button_clicked_event()
        self.get_dataset(DATABASE_PATH)
        self.show_students_database()
        self.show()

    def init_ui(self):
        self.student_qTW.setHorizontalHeaderLabels(['Matrícula', 'Nome'])
        self.student_qTW.resizeColumnsToContents()

    def button_clicked_event(self):
        self.add_student_qPB.clicked.connect(self.add_student)
        self.remove_student_qPB.clicked.connect(self.remove_student)
        self.student_qTW.itemSelectionChanged.connect(self.load_student_data)
        self.close_qPB.clicked.connect(self.close)
    
    def get_dataset(self, path):
        with open(path, encoding="utf-8") as f:
            self.database = json.load(f)
            return self.database
    
    def set_database(self, data):
        with open('database/student_data.JSON', 'w', encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    
    def show_students_database(self):
        for i, student in enumerate(self.database["students"]):
            self.insert_student(i, student["student_code"], student["student_name"])

    def add_student_database(self, code, name):
        student_id = len(self.database["students"]) + 1
        student_data = {
            "student_id": int(student_id),
            "student_code": f"{code}",
            "student_name": f"{name}",
            "attendance": False
        }
        self.database["students"].append(student_data)
        self.set_database(self.database)

    def edit_student_database(self, code, name):
        for i, student in enumerate(self.database["students"]):
            if student["student_code"] == code:
                student["student_name"] = name
                self.set_database(self.database)
                break

    def remove_student_database(self, name):
        students = self.database["students"]
        index_to_delete = next((index for (index, student) in enumerate(students) if student["student_name"] == name), None)
        if index_to_delete is not None:
            students.remove(students[index_to_delete])
            self.set_database(self.database)
      
    def add_student(self):
        code = self.student_code_qLE.text()
        name = self.student_name_qLE.text()

        if not self.is_valid_input(code, name):
            return

        row_position, existing_row = self.find_student_row(code)
        if existing_row is not None:
            self.ui.student_qTW.setItem(existing_row, 1, QTableWidgetItem(name))
            self.edit_student_database(code, name)
            self.ui.message_qLB.setText('Editado com sucesso')
        else:
            self.insert_student(row_position, code, name)
            self.add_student_database(code, name)
            self.ui.message_qLB.setText('Adicionado com sucesso')

        self.clear_input_fields()
        self.student_code_qLE.setDisabled(False)

    def remove_student(self):
        selected_items = self.ui.student_qTW.selectedItems()

        if not selected_items:
            self.ui.message_qLB.setText('Selecione um estudante')
            return
        
        name = self.student_name_qLE.text()
        self.remove_student_database(name)
        row = selected_items[0].row()
        self.ui.student_qTW.removeRow(row)
        self.ui.message_qLB.setText('Removido com sucesso')

    def is_valid_input(self, code, name):
        self.student_code_qLE.setStyleSheet('')
        self.student_name_qLE.setStyleSheet('')

        if not code or not name:
            self.ui.message_qLB.setText('Preencha os campos')
            if not code:
                self.student_code_qLE.setStyleSheet('border: 1px solid red;')
            if not name:
                self.student_name_qLE.setStyleSheet('border: 1px solid red;')
            return False

        return True

    def insert_student(self, row_position, code, name):
        self.ui.student_qTW.insertRow(row_position)
        self.ui.student_qTW.setItem(row_position, 0, QTableWidgetItem(code))
        self.ui.student_qTW.setItem(row_position, 1, QTableWidgetItem(name))

    def clear_input_fields(self):
        self.student_code_qLE.clear()
        self.student_name_qLE.clear()
        self.student_code_qLE.setStyleSheet('')
        self.student_name_qLE.setStyleSheet('')

    def find_student_row(self, code):
        row_position = self.ui.student_qTW.rowCount()
        existing_row = next(
            (
                row
                for row in range(row_position)
                if self.ui.student_qTW.item(row, 0).text() == code
            ),
            None,
        )
        return row_position, existing_row

    def load_student_data(self):
        selected_items = self.ui.student_qTW.selectedItems()
        if not selected_items:
            return
        row = selected_items[0].row()
        self.student_code_qLE.setText(self.ui.student_qTW.item(row, 0).text())
        self.student_name_qLE.setText(self.ui.student_qTW.item(row, 1).text())
        self.student_code_qLE.setDisabled(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.ui.student_qTW.rect().contains(event.pos()):
            self.ui.student_qTW.clearSelection()
            self.student_code_qLE.setDisabled(False)


if __name__ == '__main__':
    App = QApplication([])
    Home = CourseStudentListWindow()
    sys.exit(App.exec())
