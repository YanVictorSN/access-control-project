from __future__ import annotations

import os
import sys
from datetime import datetime

import cv2
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QWidget

CURRENT_FILE_PATH = os.path.abspath(__file__)
UI_PATH = os.path.join(os.path.dirname(CURRENT_FILE_PATH), 'ui', 'course_attendance_list.ui')

students_test = [
    {'name': 'Bruno', 'code': '0001'},
    {'name': 'Sara', 'code': '0002'},
    {'name': 'Vitória', 'code': '0003'},
    {'name': 'Vinicius', 'code': '0004'},
    {'name': 'Yan', 'code': '0005'}
]
class_test = 'Python 2023.1'


class AttendanceList(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi(UI_PATH, self)
        self.init_ui()
        self.button_clicked_event()
        self.start_attendance_cam()
        self.set_attendance_time()
        self.set_class_info()
        self.set_student_info()
        self.show()

    def init_ui(self):
        self.attendence_qTW.setHorizontalHeaderLabels(['Matrícula', 'Nome'])
        self.attendence_qTW.resizeColumnsToContents()

    def button_clicked_event(self):
        self.close_qPB.clicked.connect(self.cancel)

    def start_attendance_cam(self):
        self.attendance_cam = AttendanceCam()
        self.attendance_cam.start()
        self.attendance_cam.ImageUpdate.connect(self.get_image)

    def cancel(self):
        self.attendance_cam.stop()

    def get_image(self, image):
        self.camera_qL.setPixmap(QPixmap.fromImage(image))

    def set_attendance_time(self):
        current_date = datetime.now()
        current_date_formated = current_date.strftime('%d/%m/%Y')
        self.attendance_date_qL.setText(current_date_formated)

    def set_class_info(self):
        self.course_name_qL.setText(class_test)

    def set_student_info(self):
        self.attendence_qTW.setRowCount(len(students_test))

        for i, student in enumerate(students_test):
            student_name = QTableWidgetItem(student['name'])
            student_code = QTableWidgetItem(str(student['code']))
            self.attendence_qTW.setItem(i, 0, student_code)
            self.attendence_qTW.setItem(i, 1, student_name)


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
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
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
