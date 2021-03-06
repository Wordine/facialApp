import face_recognition
import cv2
import numpy as np
from PIL import Image
import threading
import time

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import methodUtils
import imgUtils

gStop = 0
gRecon = 0
gFrame = []
gImg = []
gName = ''
gArgs = ''
def screamInit(handl):
    handl.scream = QLabel(handl)
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
        global gFrame
        gFrame = frame
        
        global gStop
        if gStop :
            print ('STREAM END!')
            global gpid
            gpid = 0
            break
 
        global gRecon
        if gRecon :
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
        else:
            global gName
            global gArgs
            image = Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
            image = methodUtils.callMethod(image, gName, gArgs)

        global gImg 
        gImg = image
        
        jpg = image.toqpixmap()
        
        
        handl.scream.setPixmap(jpg)

def streamEnd():
    print ('STREAM SIGNAL!')
    global gStop, t
    gStop = 1
    try:
        t.jion()
    except Exception as e:
        pass
    
def streamStart(handlUI):
    inter=[]
    inter.append(handlUI)
    global t
    t= threading.Thread(target=streamOut, args=inter)
    t.setDaemon(True)

    global gStop
    gStop = 0
    t.start()

def getStreamStatus():
    global gStop
    return gStop

def switchRecogFlag ():
    global gRecon
    gRecon = not gRecon

def cleanRecogFlag ():
    global gRecon
    gRecon = 0

def setTrans(name, args):
    global gName
    global gArgs
    gName = name
    gArgs = args
def getOriFrame():
    global gFrame
    return gFrame

def getAfterImg():
    global gImg
    return gImg

def setFrame(handl, frame):
    if gStop == 0:
        streamEnd()
    image = Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
    global gName
    global gArgs
    jpg = methodUtils.callMethod(image, gName, gArgs)
    jpg = jpg.toqpixmap()
    jpg = jpg.scaled(handl.scream.width(), handl.scream.height())
    cleanScream(handl)
    handl.scream.setPixmap(jpg)

def cleanScream(handl):
    if gStop == 0:
        streamEnd()
    handl.scream.setPixmap(QPixmap(""))
