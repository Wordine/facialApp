# recog.py
# in: image arrary arg = "" method_name = "recog"
# out: image arrary

import face_recognition
import cv2
from PIL import Image
import sys
sys.path.append('../')

import imgUtils

def facialRecog (frame, arg) :
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_small_frame, model = 'cnn')
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    face_names = []
    for codes in face_encodings:

        name, userid = imgUtils.idVerify (codes)
        if userid == 0:
            name = "Unknown"
        face_names.append(name)

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    image = Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
        
    return image
