from __future__ import annotations

import csv
import datetime
import os
import pathlib
import pickle

import cv2
import face_recognition


class FaceRecognizer:
    def __init__(self):
        self.CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
        self.TRAINING_DATASET = pathlib.Path(self.CURRENT_FILE_PATH, 'resources', 'training_dataset')
        self.EXTRACTED_DATASET = pathlib.Path(self.CURRENT_FILE_PATH, 'resources', 'extracted_dataset')
        self.FACES_DAT = pathlib.Path(self.CURRENT_FILE_PATH, 'resources', 'faces.dat')
        self.ATTENDANCE = pathlib.Path(self.CURRENT_FILE_PATH, 'attendance')
        self.create_folders()

    def create_folders(self):
        os.makedirs(self.EXTRACTED_DATASET, exist_ok=True)
        os.makedirs(self.TRAINING_DATASET, exist_ok=True)
        os.makedirs(self.ATTENDANCE, exist_ok=True)

    def store_faces_with_names(self):
        faceClassifer = cv2.CascadeClassifier(f'{cv2.data.haarcascades}haarcascade_frontalface_default.xml')

        for imgName in pathlib.Path(self.TRAINING_DATASET).glob('*.jpg'):
            image = cv2.imread(str(imgName))
            faces = faceClassifer.detectMultiScale(image, 1.1, 5)
            name = imgName.stem
            personPath = self.EXTRACTED_DATASET / name.split('_')[0]

            if not personPath.exists():
                personPath.mkdir(parents=True)

            for x, y, width, height in faces:
                extracted_face = image[y:y + height, x:x + width]
                resized_face = cv2.resize(extracted_face, (150, 150))
                filename = f'{name}.jpg'
                filepath = str(personPath / filename)
                cv2.imwrite(filepath, resized_face)

        print('Faces extraidas e armazenadas com sucesso')

    def train_faces(self):
        directory = self.EXTRACTED_DATASET
        known_faces = []
        known_names = []

        for namePath in directory.iterdir():
            name = namePath.stem
            for imagePath in namePath.glob('*.jpg'):
                image = face_recognition.load_image_file(str(imagePath))
                face_locations = face_recognition.face_locations(image)
                face_encodings = face_recognition.face_encodings(image, face_locations)
                for encoding in face_encodings:
                    known_faces.append(encoding)
                    known_names.append(name)

        with open(self.FACES_DAT, 'wb') as f:
            pickle.dump((known_names, known_faces), f)

        print('Treinamento feito com sucesso')

    def recognize_faces(self):
        def load_known_faces():
            with open(self.FACES_DAT, 'rb') as f:
                return pickle.load(f)

        def recognize_face_names(known_names, known_faces, rgb_small_frame):
            face_names = []
            face_encodings = face_recognition.face_encodings(rgb_small_frame)
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_faces, face_encoding)
                name = 'Unknown'
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_names[first_match_index]
                face_names.append(name)
            return face_names

        def mark_attendance(name, added_names):
            today = datetime.date.today().strftime('%Y-%m-%d')
            capitalized_name = name.capitalize()
            if capitalized_name not in added_names:
                filename = f'attendance_{today}.xls'
                full_path = pathlib.Path(self.ATTENDANCE, filename)
                header_exists = full_path.exists()
                with open(full_path, mode='a', newline='') as csvfile:
                    fieldnames = ['Name', 'Date']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    if not header_exists:
                        writer.writeheader()
                    writer.writerow({'Name': capitalized_name, 'Date': today})
                added_names.add(capitalized_name)

        known_names, known_faces = load_known_faces()
        face_locations = []
        face_names = []
        process_this_frame = True
        added_names = set()
        video_capture = cv2.VideoCapture(0)

        while True:
            ret, frame = video_capture.read()
            frame = cv2.flip(frame, flipCode=1)
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]

            if process_this_frame:
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_names = recognize_face_names(known_names, known_faces, rgb_small_frame)
            process_this_frame = not process_this_frame

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top, right, bottom, left = (i * 4 for i in (top, right, bottom, left))

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)

                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1, cv2.LINE_AA)
                mark_attendance(name, added_names)

            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    fr = FaceRecognizer()
    fr.store_faces_with_names()
    fr.train_faces()
    fr.recognize_faces()
