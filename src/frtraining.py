from __future__ import annotations

import os
import pathlib
import pickle

import cv2
import face_recognition

CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
TRAINING_DATASET = pathlib.Path(CURRENT_FILE_PATH, 'resources', 'training_dataset')
EXTRACTED_DATASET = pathlib.Path(CURRENT_FILE_PATH, 'resources', 'extracted_dataset')
FACES_DAT = pathlib.Path(CURRENT_FILE_PATH, 'resources', 'faces.dat')


def store_faces_with_names():
    if not EXTRACTED_DATASET.exists():
        EXTRACTED_DATASET.mkdir()
        print(f'nova pasta: {EXTRACTED_DATASET}')

    faceClassifer = cv2.CascadeClassifier(f'{cv2.data.haarcascades}haarcascade_frontalface_default.xml')

    for imgName in pathlib.Path(TRAINING_DATASET).glob('*.jpg'):
        imagem = cv2.imread(str(imgName))
        faces = faceClassifer.detectMultiScale(imagem, 1.1, 5)

        name = imgName.stem
        personPath = EXTRACTED_DATASET / name.split('_')[0]
        if not personPath.exists():
            personPath.mkdir(parents=True)

        for x, y, a, l in faces:
            face = imagem[y:y + l, x:x + a]
            face = cv2.resize(face, (150, 150))
            cv2.imwrite(str(personPath / f'{name}.jpg'), face)

    print('Faces extraidas e armazenadas com sucesso')


def train_faces():
    directory = EXTRACTED_DATASET
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

    with open(pathlib.Path(FACES_DAT), 'wb') as f:
        pickle.dump((known_names, known_faces), f)

    print('Treinamento feito com sucesso')


def recognize_faces():
    # Load the known faces and embeddings
    with open(pathlib.Path(FACES_DAT), 'rb') as f:
        known_names, known_faces = pickle.load(f)

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    # Start capturing the video stream
    video_capture = cv2.VideoCapture(0)
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()
        frame = cv2.flip(frame, flipCode=1)  # Flip the image horizontally

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known faces
                matches = face_recognition.compare_faces(known_faces, face_encoding)
                name = 'Unknown'

                # If a match was found in known_faces, just use the first one
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_names[first_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        # Draw a box around the faces
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    store_faces_with_names()
    train_faces()
    recognize_faces()
