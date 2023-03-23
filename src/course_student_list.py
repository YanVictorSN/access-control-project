from __future__ import annotations

import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QWidget


UI_PATH = 'ui/course_student_list.ui'


class CourseStudentListWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi(UI_PATH, self)
        self.student_qTW.setHorizontalHeaderLabels(['Matrícula', 'Nome'])
        self.button_clicked_event()
        self.show()

    def button_clicked_event(self):
        self.add_student_qPB.clicked.connect(self.add_student)
        self.remove_student_qPB.clicked.connect(self.remove_student)
        self.close_qPB.clicked.connect(self.close)

    def add_student(self):
        code = self.student_code_qLE.text()
        name = self.student_name_qLE.text()

        if not self.is_valid_input(code, name):
            return

        self.insert_student(code, name)
        self.clear_input_fields()
        self.ui.message_qLB.setText('Estudante adicionado')

    def remove_student(self):
        selected_items = self.ui.student_qTW.selectedItems()

        if not selected_items:
            self.ui.message_qLB.setText('Selecione um estudante')
            return

        row = selected_items[0].row()
        self.ui.student_qTW.removeRow(row)
        self.ui.message_qLB.setText('Estudante removido')

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

    def insert_student(self, code, name):
        row_position = self.ui.student_qTW.rowCount()
        self.ui.student_qTW.insertRow(row_position)
        self.ui.student_qTW.setItem(row_position, 0, QTableWidgetItem(code))
        self.ui.student_qTW.setItem(row_position, 1, QTableWidgetItem(name))

    def clear_input_fields(self):
        self.student_code_qLE.clear()
        self.student_name_qLE.clear()
        self.student_code_qLE.setStyleSheet('')
        self.student_name_qLE.setStyleSheet('')


if __name__ == '__main__':
    App = QApplication([])
    Home = CourseStudentListWindow()
    sys.exit(App.exec())
