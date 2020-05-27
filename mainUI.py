import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PIL import Image

import numpy as np
import cv2
import face_recognition

import mainScream
import imgUtils
import imgSelect
import methodUtils

class picture(QMainWindow):
    def __init__(self):
        super(picture, self ).__init__()
        
        self.resize(1280, 720)
        self.setWindowTitle("facial recog system")
        
        mainScream.screamInit(self)
        self.messageShow('sucessfully start system', 0)
        self.actionInit()
        self.menuInit(0)
        self.toolbarInit(0)

        self.startStream()
        
    #status 0:camera 
    #status 1:catched a photo
    def loginProcess(self):
        checklist = []
        if mainScream.getStreamStatus() == 0:
            mainScream.streamEnd()
            idIMG = mainScream.getOriFrame()
            mainScream.setFrame(self, idIMG)

            
        elif mainScream.getStreamStatus() == 1:
            idIMG = mainScream.getOriFrame()
            pass

        img = idIMG[:, :, ::-1]
        locations = face_recognition.face_locations(img, model = 'cnn')
        encodings = face_recognition.face_encodings(img, locations)

        checklist = []
        for (top, right, bottom, left), code in zip(locations, encodings):
            username, userid = imgUtils.idVerify(code)
            img_slice = idIMG[top:bottom, left:right]
            userinfo = { 'userid': userid, 'username': username,'img': img_slice, 'code': code}  
            checklist.append(userinfo)

        dialog = QtWidgets.QDialog()
        ui = imgSelect.Ui_imgSelect()
        ui.setupUi(dialog, checklist, 0)
        ret = dialog.exec_()
        if ret == 0:
            self.startStream()

        elif ret == 1:
            idx = ui.comboBox.currentIndex()
            userinfo = checklist[idx]
            if userid == 0:
                self.addUser()
            else:
                self.userinfo = userinfo
            # get userfile from db
            self.userFileList = imgUtils.getUserFile(self.userinfo["userid"], 3)

            # nothing found in userFiles
            if len(self.userFileList) == 0:
                self.idx = 0
                mainScream.cleanScream(self)
            else:
                # display the first img
                frame = self.userFileList[0]["img"]
                mainScream.setFrame(self, frame)
                self.idx = 0 
            self.menuInit(1)
            self.toolbarInit(1)

    def loginFromImg(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
        if imgName == "":
            return 0
        imgName = imgName.convertToFormat(QImage.Format.Format_RGBA8888)
        width = imgName.width()
        height = imgName.height()
        ptr = imgName.bits()
        ptr.setsize(height * width * 4)
        frame = np.frombuffer(ptr, np.uint8).reshape((height, width, 4))

        mainScream.setFrame(self, frame)


    def loginFromStream(self):
        if mainScream.getStreamStatus == 0:
            return 0
        self.startStream()

    def logoutProcess(self):
        self.userinfo = []
        self.idx = -1
        self.toolbarInit(2)
        self.menuInit(2)
        mainScream.setTrans()
        if mainScream.getStreamStatus == 1:
            mainScream.streamStart()


    def addImg(self):
        image = mainScream.getAfterImg()
        image = np.array(image)

        imgUtils.saveUserFile(self.userinfo["userid"], 1, image)
        self.userFileList = imgUtils.getUserFile(self.userinfo["userid"], 3)

    def selectTransMethod(self, method):
        mthList = methodList.getMethodList()
        dialog = QtWidgets.QDialog()
        ui = imgSelect.Ui_imgSelect()
        ui.setupUi(dialog, self.userFileList, 2)
        ret = dialog.exec_()
        if ret == 0:
            return 0
        else:
            idx = ui.comboBox.currentIndex()
            name = mthList[idx]["name"]
            args = mthList[idx]["args"]
            mainScream.setTrans(name, args)

    
    def selectImg(self):
        if len(self.userFileList) == 0:
            self.messageShow("you should add your img first!", 1)
            return 0
        dialog = QtWidgets.QDialog()
        ui = imgSelect.Ui_imgSelect()
        ui.setupUi(dialog, self.userFileList, 1)
        ret = dialog.exec_()
        if ret == 0:
            return 0
        else:
            idx = ui.comboBox.currentIndex() 
            frame = self.userFileList[idx]["img"]
            if mainScream.getStreamStatus == 0:
                mainScream.streamEnd()
            mainScream.setFrame(self, frame)

    def delImg(self):
        if len(self.userFileList) == 0:
            self.messageShow("you should add your img first!", 1)
            return 0
        dialog = QtWidgets.QDialog()
        ui = imgSelect.Ui_imgSelect()
        ui.setupUi(dialog, self.userFileList, 1)
        ret = dialog.exec_()
        if ret == 0:
            return 0
        else:
            idx = ui.comboBox.currentIndex() 
            userid = self.userinfo['userid']
            pid = self.userFileList[idx]['id']
            imgUtils.del_pic(pid, userid)
            self.userFileList = imgUtils.getUserFile(self.userinfo["userid"], 3)

    #flag 0:init  1:normal message  2:warring message
    def messageShow(self, message, flag):
        if flag == 0:
            self.messagelb = QLabel(self)
            self.messagelb.setFixedSize(200, 480)
            self.messagelb.move(800, 60)
            self.messagelb.setStyleSheet("color:black")
            self.messagelb.setText(message)
            # self.setWordWrap(True)
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
            self.delImgBar = self.addToolBar('del img')
            self.delImgBar.addAction(self.delImgAction)
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
        self.delImgAction = QAction(QIcon('icon/1222526.png'), 'del img', self)
        self.delImgAction.setStatusTip('del an img from your files')
        self.delImgAction.triggered.connect(self.delImg)
        self.tranImgAction = QAction(QIcon('icon/1222534.png'), 'transform', self)
        self.tranImgAction.setStatusTip('select a method')
        self.tranImgAction.triggered.connect(self.selectTransMethod)

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
