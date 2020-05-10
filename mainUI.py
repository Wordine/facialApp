import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import mainScream
import imgUtils
import numpy as np
global my

class picture(QWidget):
    def __init__(self):
        super(picture, self ).__init__()
        
        self.resize(1280, 720)
        self.setWindowTitle("facial recog system")
        
        mainScream.screamInit(self)
        self.messageShow('sucessfully start system', 0)
        self.menuInit(0)
        self.toolbarInit(0)

        self.startStream()
        
    #status 0:camera 
    #status 1:catched a photo
    def loginProcess(self):
        checklist = []
        if mainScream.getStreamStatus() == 0:
            mainScream.streamEnd()

            idIMG = self.frame

            image = Image.fromarray(cv2.cvtColor(idIMG,cv2.COLOR_BGR2RGB))
            jpg = image.toqpixmap()
            self.scream.setPixmap(jpg)
            
        elif mainScream.getStreamStatus() == 1:
            idIMG = self.frame
            pass

        img = idIMG[:, :, ::-1]
        locations = face_recognition.face_locations(img, model = 'cnn')
        encodings = face_recognition.face_encodings(img, locations)

        checklist = []
        for (top, right, bottom, left), code in zip(locations, encodings):
            username, userid = imgUtils.idVerify(code)
            img_slice = idIMG[top:bottom, left:right]
            userinfo["userid"]   = userid
            userinfo["username"] = username
            userinfo["img"]      = img_slice
            userinfo["code"]     = code
            checklist.append(userinfo)

        dialog = QtWidgets.QDialog()
        ui = imgSelect.Ui_imgSelect()
        ui.setupUi(dialog, checklist)
        ret = dialog.exec_()
        if ret == 0:
            self.startStream()

        elif ret == 1:
            idx = ui.comboBox.currentIndex()
            userinfo = checklist[idx]
            if userid == 0:
                #create new user

            else:
                self.userinfo = userinfo
            self.userFileList = imgUtils.getUserFile(self.userinfo["userid"], 3)
            if len(self.userFileList) == 0:
                #blank mainScream
                self.idx = -1
            else:
                #show first img
                self.idx = 0 

    def loginFromImg(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
        if imgName == "":
            return 0
        imgName = imgName.convertToFormat(QImage.Format.Format_RGBA8888)
        width = imgName.width()
        height = imgName.height()
        ptr = imgName.bits()
        ptr.setsize(height * width * 4)
        self.frame = np.frombuffer(ptr, np.uint8).reshape((height, width, 4))

        jpg = QtGui.QPixmap(imgName).scaled(self.scream.width(), self.scream.height())
        self.stopStream()
        self.scream.setPixmap(jpg)

    def loginFromStream(self):
        self.startStream()

    def logoutProcess(self):
        self.userinfo = []
        self.idx = -1
        self.toolbarInit(0)
        self.menuInit(0)


    def addImg(self):
        if mainScream.getStreamStatus == 0:
            mainScream.streamEnd()

            idIMG = self.frame
            image = Image.fromarray(cv2.cvtColor(idIMG,cv2.COLOR_BGR2RGB))
            jpg = image.toqpixmap()
            self.scream.setPixmap(jpg)
            
        elif mainScream.getStreamStatus == 1:
            idIMG = self.frame
            pass

        imgUtils.saveUserFile(idIMG)
        self.userFileList = imgUtils.getUserFile(self.userinfo["userid"], 3)
        self.idx = len(self.userFileList) - 1

    def photoTransProcess(self, arg):
        img = methodUtils.callMethod (self.frame, self.checkMethod, arg)

        imgUtils.saveUserFile(self.userid, 2, img)

    def selectTransMethod(self, method):
    
    def selectImg(self):
        if self.userFileList == "":
            self.messageShow("you should add your img first!", 1)
            return 0
        dialog = QtWidgets.QDialog()
        ui = imgSelect.Ui_imgSelect()
        ui.setupUi(dialog, self.userFileList)
        ret = dialog.exec_()
        if ret == 0:
            return 0
        else
            self.idx = ui.comboBox.currentIndex() 
            self.frame = self.userFileList[0]["img"]
            image = Image.fromarray(cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB))
            jpg = QtGui.QPixmap(image).scaled(self.scream.width(), self.scream.height())
            self.scream.setPixmap(jpg)

    

    #flag 0:init  1:normal message  2:warring message
    def messageShow(self, message, flag):

    #flag 0:init  1:unverfied  2:verified
    def menuInit(self, flag):
        self.menubar.clear()
        
        sourceMenu = self.menubar.addMenu('Source')
        recogMenu  = self.menubar.addMenu('high light')
            
    #flag 0:init   1:before login    2:login
    def toolbarInit(self, flag):

    def actionInit(self):
        self.statusBar()

        self.menubar = self.menuBar()

        self.loginAction        = 
        self.regFromVideoAction = 
        self.regFromImgAction   = 

        self.exitActionAction   =
        self.addFromImgAction   =
        self.addFromVideoAction =

        self.selectImgAction    =
        self.tranImgAction      =

    def startStream(self):
        print("enter subprocess")
        mainScream.streamStart(self)

    def stopStream(self):
        print('send stop signal')
        mainScream.streamEnd()

    def switchRecog(self):
        mainScream.switchRecogFlag()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my = picture()
    my.show()
    
    sys.exit(app.exec_())
