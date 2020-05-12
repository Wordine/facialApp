import face_recognition
import cv2
import numpy as np
from PIL import Image
import threading
import time
from PyQt5.QtGui import *

import imgUtils

gStop = 0
gRecon = 0

def screamInit(handl):
    handl.scream = QLabel(self)
    handl.scream.setText("wait for init.....")
    handl.scream.setFixedSize(640, 480)
    handl.scream.move(160, 60)
      
    handl.scream.setStyleSheet("QLabel{background:white;}"
                               "QLabel{font-size:10px;font-weight:bold;font-family:宋体;}")

def streamOut(handl):
    video_capture = cv2.VideoCapture(0)
    print ('subprocess start')
    while True:
        ret, frame = video_capture.read()
        handl.frame = frame
        
        global gStop
        if gStop :
            print ('STREAM END!')
            break
 
        global gRecon
        if gRecon :
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_small_frame, model = 'cnn')
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

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
        
        jpg = image.toqpixmap()
        
        
        handl.scream.setPixmap(jpg)

def streamEnd():
    print ('STREAM SIGNAL!')
    global gStop
    gStop = 1
    
def streamStart(handlUI):
    inter=[]
    inter.append(handlUI)
    t= threading.Thread(target=streamOut, args=inter)
    t.setDaemon(True)
    t.start()

def getStreamStatus():
    global gStop
    return gStop

def switchRecogFlag ():
    global gRecon
    gRecon = not gRecon




