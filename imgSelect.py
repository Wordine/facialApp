# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'imgSelect.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class Ui_imgSelect(object):
    def setupUi(self, imgSelect):
        imgSelect.setObjectName("imgSelect")
        imgSelect.resize(738, 544)
        self.buttonBox = QtWidgets.QDialogButtonBox(imgSelect)
        self.buttonBox.setGeometry(QtCore.QRect(80, 490, 621, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.graphicsView = QtWidgets.QGraphicsView(imgSelect)
        self.graphicsView.setGeometry(QtCore.QRect(20, 20, 561, 441))
        self.graphicsView.setObjectName("graphicsView")
        
        self.comboBox = QtWidgets.QComboBox(imgSelect)
        self.comboBox.setGeometry(QtCore.QRect(620, 90, 87, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("1")
        self.comboBox.addItem("2")
        self.comboBox.addItem("3")
        self.comboBox.addItem("4")
        self.comboBox.addItem("5")
        self.comboBox.addItem("6")
        self.comboBox.addItem("7")
        
        self.retranslateUi(imgSelect)
        self.buttonBox.accepted.connect(imgSelect.accept)
        self.buttonBox.rejected.connect(imgSelect.reject)
        QtCore.QMetaObject.connectSlotsByName(imgSelect)

    def retranslateUi(self, imgSelect):
        _translate = QtCore.QCoreApplication.translate
        imgSelect.setWindowTitle(_translate("imgSelect", "Dialog"))
        
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
