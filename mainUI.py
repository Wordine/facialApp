import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import mainScream
import imgUtils

global my

class picture(QWidget):
    def __init__(self):
        super(picture, self ).__init__()
        
        self.resize(1280, 720)
        self.setWindowTitle("label显示图片")
        
        self.scream = QLabel(self)
        self.scream.setText("   显示图片")
        self.scream.setFixedSize(640, 480)
        self.scream.move(160, 160)
        
        self.scream.setStyleSheet("QLabel{background:white;}"
                                 "QLabel{color:rgb(300,300,300,120);font-size:10px;font-weight:bold;font-family:宋体;}"
                                 )
        
        """
        btn = QPushButton(self)
        btn.setText("打开图片")
        btn.move(10, 30)
        btn.clicked.connect(self.stopStream)
        """

        self.leftUI()
        self.upperUI(0)
        self.messageShow('sucessfully start system', 0)
        self.rightUI(0)


        self.startStream()
        
    def openimage(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
        print(imgName)
        print(imgType)
        jpg = QtGui.QPixmap(imgName).scaled(self.scream.width(), self.scream.height())
        self.scream.setPixmap(jpg)
        
    #status 1:wait for camera to catch a photo
    #status 2:catched a photo
    def loginProcess(self):
        self.checkList = []
        if self.status == 1:
            idIMG = self.frame
            self.scream.setPixmap(idIMG)
            self.checkList = idVerify (idIMG)

            ###Create Combo Box###
            
        elif self.status == 2:
            # when new guy sign in
            if new guy:
            elif old guy:
                # the old guy
                for x in self.checkList:
                    if x.name == self.checkName:
                        IMG = x.IMG
                        name = x.name
                        break
            
            ###show message to user to check###
            if pass:
            else:
                self.statusJumper (1)

            

        
        
    #type 1:Origin    type 2:transformed
    def showPhotoList(self, type):
        
    def photoTransProcess(self, arg):
        img = methodUtils.callMethod (self.frame, self.checkMethod, arg)

        imgUtils.saveUserFile(self.userid, 2, img)
        
        
    def selectCheckName(self, name):
        self.checkName = name

    def selectTransMethod(self, method):
        self.checkMethod = method
        ###flush rightUI###
    
    """
    0:camera stream

    1:captured img

    2:login sucessfully

    3:selected method
    """
    def statusJumper (self, flag):
        if flag == 0:
            # give up captured img

            # logout


        elif flag == 1:
            #camera catch a photo
            #choose to open a image

        elif flag == 2:
            #sucessfully login
            #sucessfully transformed

        elif flag == 3:
            #select a method

        else:
            self.messageShow('STATUS JUMPER ERROR, wrong flag' + str(flag), 2)
        
    #flag 0:init  1:normal message  2:warring message
    def messageShow(self, message, flag):

    def leftUI (self):
        switchRecogBtn
    
    #flag 0:init  1:unverfied  2:verified
    def upperUI (self, flag):
        inputMethodMenu

        logoutMenu

        imgTypeSelectMenu


    #flag 0:init   1:return camera   2:captured img   3:origin   4:selected method    
    def rightUI (self, flag):
        loginBtn

        selectNameCombo

        selectMethodCombo



    def startStream(self):
        print('enter subprocess')
        mainScream.streamStart(self)

    def stopStream(self):
        print('send stop signal')
        mainScream.streamEnd()

    def setRecog(self):
        mainScream.setRecogFlag(flag)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my = picture()
    my.show()
    
    sys.exit(app.exec_())
