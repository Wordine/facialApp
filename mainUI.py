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
                pass
            else:
                self.userinfo = userinfo

            self.userFileList = imgUtils.getUserFile(self.userinfo["userid"], 3)
            if len(self.userFileList) == 0:
                #blank mainScream
                self.idx = -1
            else:
                #show first img
                self.idx = 0 
            self.menuInit(1)
            selg.toolbarInit(1)

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
        self.toolbarInit(2)
        self.menuInit(2)


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
        return 0
    
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
        else:
            self.idx = ui.comboBox.currentIndex() 
            self.frame = self.userFileList[0]["img"]
            image = Image.fromarray(cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB))
            jpg = QtGui.QPixmap(image).scaled(self.scream.width(), self.scream.height())
            self.scream.setPixmap(jpg)

    

    #flag 0:init  1:normal message  2:warring message
    def messageShow(self, message, flag):
        if flag == 0:
            self.messagelb = QLabel(self)
            self.messagelb.setFixedSize(200, 480)
            self.messagelb.move(800, 60)
            self.messagelb.setStyleSheet("color:black")
            self.messagelb.setText(message)
            self.setWordWrap(True)
        elif flag == 1:
            self.messagelb.setStyleSheet("color:black")
            self.messagelb.setText(message)

        elif flag == 2:
            self.messagelb.setStyleSheet("color:red")
            self.messagelb.setText(message)

    #flag 0:init  1:unverfied  2:verified
    def menuInit(self, flag):

        if flag == 0:
            self.menubar = self.menuBar()
            sourceMenu = self.menubar.addMenu('Source')
            sourceMenu.addAction(self.regFromImgAction)
            sourceMenu.addAction(self.regFromVideoAction)

            recogMenu = self.menubar.addMenu('high light')
            recogMenu.addAction(self.switchRecogAction)

        elif flag == 1:
            self.menubar.clear()
            sourceMenu = self.menubar.addMenu('Source')
            sourceMenu.addAction(self.regFromImgAction)
            sourceMenu.addAction(self.regFromVideoAction)
        elif flag == 2:
            self.menubar.clear()
            sourceMenu = self.menubar.addMenu('Source')
            sourceMenu.addAction(self.regFromImgAction)
            sourceMenu.addAction(self.regFromVideoAction)

            recogMenu = self.menubar.addMenu('high light')
            recogMenu.addAction(self.switchRecogAction)
        
    #flag 0:init   1:before login    2:login
    def toolbarInit(self, flag):
        if flag == 0:
            self.loginBar = self.addToolBar('login')
            self.loginBar.addAction(self.loginAction)

        elif flag == 1:
            self.loginBar.clear()
            self.loginBar = self.addToolBar('logout')
            self.loginBar .addAction(self.exitActionAction)
            self.addImgBar = self.addToolBar('add')
            self.addImgBar.addAction(self.addImgAction)
            self.selectImgBar = self.addToolBar('select img')
            self.selectImgBar.addAction(self.selectImgAction)
            self.transBar = self.addToolBar('select method')
            self.transBar.addAction(self.tranImgAction)

        elif flag == 2:
            self.loginBar.clear()
            self.addImgBar.clear()
            self.selectImgBar.clear()
            self.transBar.clear()

            self.loginBar = self.addToolBar('login')
            self.loginBar.addAction(self.loginAction)

    def actionInit(self):
        self.statusBar()

        self.menubar = self.menuBar()

        self.loginAction = QAction(QIcon('icon/1222569.png'), 'login', self)
        self.loginAction.setStatusTip('login in')
        self.loginAction.triggered.connect(self.loginProcess)
        self.regFromVideoAction = QAction(QIcon('icon/1222540.png'), 'video', self)
        self.regFromVideoAction.setStatusTip('load img from video')
        self.regFromVideoAction.triggered.connect(self.loginFromStream)
        self.regFromImgAction = QAction(QIcon('icon/1222831.png'), 'file', self)
        self.regFromImgAction.setStatusTip('load img from file')
        self.regFromImgAction.triggered.connect(self.loginFromImg)

        self.exitActionAction = QAction(QIcon('icon/1222539.png'), 'exit', self)
        self.exitActionAction.setStatusTip('logout')
        self.exitActionAction.triggered.connect(self.logoutProcess)
        self.addImgAction = QAction(QIcon('icon/1222532.png'), 'add', self)
        self.addImgAction.setStatusTip('add img')
        self.addImgAction.triggered.connect(self.addImg)

        self.selectImgAction = QAction(QIcon('icon/1222538.png'), 'select img', self)
        self.selectImgAction.setStatusTip('select an img from your files')
        self.selectImgAction.triggered.connect(self.selectImg)
        self.tranImgAction = QAction(QIcon('icon/1222534.png'), 'transform', self)
        self.tranImgAction.setStatusTip('tranform your img')
        self.tranImgAction.triggered.connect(self.photoTransProcess)

        self.switchRecogAction = QAction(QIcon('icon/1222531.png'), 'switch', self)
        self.switchRecogAction.setStatusTip('switch recog set')
        self.switchRecogAction.triggered.connect(self.switchRecog)

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
