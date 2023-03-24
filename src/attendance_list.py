from __future__ import annotations

# import os
import sys
import cv2

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QWidget
from datetime import datetime

UI_PATH = 'ui/attendance_list.ui'

students_test = [
    {"name": "Bruno", "registration_number": "0001"},
    {"name": "Sara", "registration_number": "0002"},
    {"name": "Vitória", "registration_number": "0003"},
    {"name": "Vinicius", "registration_number": "0004"},
    {"name": "Yan", "registration_number": "0005"}
]


class AttendanceList(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi(UI_PATH, self)
        self.show()
        self.set_attendance_cam()
        self.set_attendance_time()
        self.set_class_info()
        self.set_student_info()

    def set_attendance_cam(self):
        self.attendance = AttendanceCam()
        self.attendance.start()
        self.attendance.ImageUpdate.connect(self.get_image)

    def get_image(self, image):
        self.attendanceCamera_QL.setPixmap(QPixmap.fromImage(image))
    
    def set_attendance_time(self):
        current_time = datetime.now()
        current_time_formated = current_time.strftime('%d/%m/%Y %H:%M:%S')
        self.dataInfo_QL.setText(f'Data: {current_time_formated} ')

    def set_class_info(self):
        self.classInfo_QL.setText('Turma: Python 2023.1 ')
  
    def set_student_info(self):
        self.attendanceListTable.setRowCount(len(students_test)) 

        for i, student in enumerate(students_test):
            student_name = QTableWidgetItem(student['name'])
            registration_number = QTableWidgetItem(str(student['registration_number']))
            self.attendanceListTable.setItem(i, 0, registration_number)
            self.attendanceListTable.setItem(i, 1, student_name)


class AttendanceCam(QThread):
    ImageUpdate = pyqtSignal(QImage)

    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(
                    FlippedImage.data,
                    FlippedImage.shape[1],
                    FlippedImage.shape[0],
                    QImage.Format_RGB888
                )
                Pic = ConvertToQtFormat.scaled(400, 300, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
        Capture.release()

    def stop(self):
        self.ThreadActive = False
        self.wait()
        self.quit()


if __name__ == '__main__':
    App = QApplication([])
    Home = AttendanceList()
    sys.exit(App.exec())