import face_recognition
import cv2
import numpy as np
import threading
import time
from PyQt5.QtGui import *

gStop = 0
gRecon = 0

def screamInit(handl):
        handl.scream = QLabel(self)
        handl.scream.setText("wait for init.....")
        handl.scream.setFixedSize(640, 480)
        handl.scream.move(160, 160)
        
        handl.scream.setStyleSheet("QLabel{background:white;}"
                                 "QLabel{color:rgb(300,300,300,120);font-size:10px;font-weight:bold;font-family:宋体;}"
                                 )

def streamOut(handl):
    video_capture = cv2.VideoCapture(0)
    print ('subprocess start')
    while True:
        ret, frame = video_capture.read()
        
        height, width, channel = frame.shape
        by(qImg)
        tesPerLine = 3 * width
        qImg = QImage(frame, width, height, bytesPerLine, QImage.Format_RGB888)
        jpg = QPixmap
        
        handl.frame = jpg
        handl.scream.setPixmap(jpg)
        
        global gStop
        if gStop :
            print ('STREAM END!')
            break
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

def switchRecogFlag ():
    global gRecon
    gRecon = not gRecon




