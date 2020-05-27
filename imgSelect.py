# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'imgSelect.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
from PIL import Image
import cv2


class Ui_imgSelect(object):
    # flag:0 who   flag:1 which picture
    def setupUi(self, imgSelect, checklist, flag):
        imgSelect.setObjectName("imgSelect")
        imgSelect.resize(738, 544)
        self.buttonBox = QtWidgets.QDialogButtonBox(imgSelect)
        self.buttonBox.setGeometry(QtCore.QRect(80, 490, 621, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.scream = QLabel(imgSelect)
        self.scream.move( 20, 20)
        
        self.comboBox = QtWidgets.QComboBox(imgSelect)
        self.comboBox.setGeometry(QtCore.QRect(620, 90, 87, 22))
        self.comboBox.setObjectName("comboBox")
        
        self.check = checklist
        for item in checklist:
            if flag == 0:
                self.comboBox.addItem(item["username"])
                self.comboBox.currentIndexChanged.connect(self.comboFlushImg)
            elif flag == 1:
                self.comboBox.addItem(item["id"])
                self.comboBox.currentIndexChanged.connect(self.comboFlushImg)
            elif flag == 2:
                self.comboBox.addItem(item["name"])
                self.comboBox.currentIndexChanged.connect(self.comboFlushImg)
        
        
        self.retranslateUi(imgSelect)
        self.buttonBox.accepted.connect(imgSelect.accept)
        self.buttonBox.rejected.connect(imgSelect.reject)
        QtCore.QMetaObject.connectSlotsByName(imgSelect)

        image = self.check[0]["img"]
        image = image[:, :, ::-1]
        image = Image.fromarray(image)
        jpg = image.toqpixmap()
        self.scream.setPixmap(jpg)

    def retranslateUi(self, imgSelect):
        _translate = QtCore.QCoreApplication.translate
        imgSelect.setWindowTitle(_translate("imgSelect", "Dialog"))
    def comboFlushImg(self):
        idx = self.comboBox.currentIndex()

        image = self.check[idx]["img"]
        image = image[:, :, ::-1]
        image = Image.fromarray(image)
        jpg = image.toqpixmap()
        self.scream.setPixmap(jpg)


def main():
    """
    主函数，用于运行程序
    :return: None
    """
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    ui = Ui_imgSelect()
    ui.setupUi(dialog)
    dialog.show()
    ret = dialog.exec_()
    if ret == 0:
        print ("denied")
    elif ret == 1:
        print ("system end with return value = ", str(ui.comboBox.currentIndex()))
    sys.exit()


if __name__ == '__main__':
    main()
