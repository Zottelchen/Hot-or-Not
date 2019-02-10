# -*- coding: utf-8 -*-

import ctypes
import os
import shutil
import sys
from glob import glob

from PyQt5 import QtCore, QtGui, QtWidgets

directory = ""
currentFile = ""
myappid = u'hawtornawt'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 900)
        MainWindow.setMinimumSize(QtCore.QSize(1600, 900))
        MainWindow.setMaximumSize(QtCore.QSize(1600, 900))
        MainWindow.setWindowTitle("Hawt Or Nawt (Version 1.0)")
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setWindowIcon(QtGui.QIcon(resource_path('./flame.ico')))
        MainWindow.setStyleSheet("background: rgb(125, 125, 125);\n"
                                 "font: 10pt \"Verdana\";\n"
                                 "color: rgb(223, 223, 223)")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.loadButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadButton.setGeometry(QtCore.QRect(750, 830, 110, 30))
        self.loadButton.setObjectName("loadButton")
        self.nawtButton = QtWidgets.QPushButton(self.centralwidget)
        self.nawtButton.setGeometry(QtCore.QRect(0, 400, 100, 30))
        self.nawtButton.setStyleSheet("color: rgb(255, 147, 149);")
        self.nawtButton.setObjectName("nawtButton")
        self.hawtButton = QtWidgets.QPushButton(self.centralwidget)
        self.hawtButton.setGeometry(QtCore.QRect(1500, 400, 100, 30))
        self.hawtButton.setStyleSheet("color: rgb(165, 213, 151)")
        self.hawtButton.setObjectName("hawtButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 0, 1380, 820))
        self.label.setStyleSheet("background-color: rgb(85, 85, 85);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.loadButton.clicked.connect(self.loadPath)
        self.hawtButton.clicked.connect(self.hawt)
        self.nawtButton.clicked.connect(self.nawt)

        self.hawtButton.setEnabled(False)
        self.nawtButton.setEnabled(False)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.loadButton.setText(_translate("MainWindow", "Load Folder"))
        self.nawtButton.setText(_translate("MainWindow", "☒Nawt"))
        self.nawtButton.setShortcut(_translate("MainWindow", "Left"))
        self.hawtButton.setText(_translate("MainWindow", "❤Hawt"))
        self.hawtButton.setShortcut(_translate("MainWindow", "Right"))
        self.label.setText(_translate("MainWindow", "No folder loaded"))

    def loadPath(self):
        global directory
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "Open Dir", "C:/")
        # print("CHOSEN DIR: " + directory)
        if not os.path.exists(directory + "/hawt"):
            os.makedirs(directory + "/hawt")
        if not os.path.exists(directory + "/nawt"):
            os.makedirs(directory + "/nawt")
        # print("CREATED FOLDERS")
        self.hawtButton.setEnabled(True)
        self.nawtButton.setEnabled(True)
        self.loadNextImage()

    def loadNextImage(self):
        global currentFile
        cwd = glob(directory + "/*.png")
        cwd.extend(glob(directory + '/*.jpg'))
        cwd.extend(glob(directory + '/*.jpeg'))
        # print("CWD: " + str(cwd))
        if len(cwd) == 0:
            self.hawtButton.setEnabled(False)
            self.nawtButton.setEnabled(False)
            self.label.setText("No more images. Choose new folder.")
            # print("ALL DONE!")
            return
        currentFile = cwd[0]

        # print("CWD: " + currentFile)
        myPixmap = QtGui.QPixmap(currentFile)
        # print("Imageprofile created")
        myScaledPixmap = myPixmap.scaled(self.label.size(), QtCore.Qt.KeepAspectRatio)
        # print("Imageprofile scaled")
        self.label.setPixmap(myScaledPixmap)

    def hawt(self):
        # print("hawt: " + currentFile + "   " + os.path.basename(currentFile))
        shutil.move(currentFile, directory + "/hawt/" + os.path.basename(currentFile))
        self.loadNextImage()

    def nawt(self):
        # print("nawt: " + currentFile + "   " + os.path.basename(currentFile))
        shutil.move(currentFile, directory + "/nawt/" + os.path.basename(currentFile))
        self.loadNextImage()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


