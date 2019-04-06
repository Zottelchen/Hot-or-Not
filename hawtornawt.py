# -*- coding: utf-8 -*-

import ctypes
import os
import shutil
import sys
from glob import glob

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from easysettings import EasySettings
from pathlib2 import Path

directory = ""
currentFile = ""
previousFile = ""
myappid = u'hawtornawt'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
settings = EasySettings("hawtornawt.conf")


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        global previousFile
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 900)
        MainWindow.setMinimumSize(QtCore.QSize(1600, 900))
        MainWindow.setMaximumSize(QtCore.QSize(1600, 900))
        MainWindow.setWindowTitle("Hawt Or Nawt (Version 1.2)")
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setWindowIcon(QtGui.QIcon(resource_path('./flame.ico')))
        MainWindow.setStyleSheet("background: rgb(125, 125, 125);\n"
                                 "font: 10pt \"Verdana\";\n"
                                 "color: rgb(223, 223, 223)")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.loadButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadButton.setGeometry(QtCore.QRect(810, 820, 110, 30))
        self.loadButton.setObjectName("loadButton")
        self.undoButton = QtWidgets.QPushButton(self.centralwidget)
        self.undoButton.setGeometry(QtCore.QRect(700, 820, 110, 30))
        self.undoButton.setStyleSheet("color: rgb(254, 248, 140);")
        self.undoButton.setObjectName("undoButton")
        self.nawtButton = QtWidgets.QPushButton(self.centralwidget)
        self.nawtButton.setGeometry(QtCore.QRect(0, 400, 100, 30))
        self.nawtButton.setStyleSheet("color: rgb(255, 147, 149);")
        self.nawtButton.setObjectName("nawtButton")
        self.clearnawtButton = QtWidgets.QPushButton(self.centralwidget)
        self.clearnawtButton.setGeometry(QtCore.QRect(0, 460, 100, 30))
        self.clearnawtButton.setStyleSheet("color: rgb(255, 147, 149);")
        self.clearnawtButton.setObjectName("nawtButton")
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

        self.totalcount = QtWidgets.QLabel(self.centralwidget)
        self.totalcount.setGeometry(750, 850, 150, 30)
        # self.count.setText("Count: xxx")

        self.hawtcount = QtWidgets.QLabel(self.centralwidget)
        self.hawtcount.setGeometry(QtCore.QRect(1500, 430, 100, 30))
        # self.hawtcount.setText("Hawt: xxx")
        self.nawtcount = QtWidgets.QLabel(self.centralwidget)
        self.nawtcount.setGeometry(QtCore.QRect(0, 430, 100, 30))
        # self.nawtcount.setText("Nawt: xxx")

        self.loadButton.clicked.connect(self.loadPath)
        self.hawtButton.clicked.connect(self.hawt)
        self.nawtButton.clicked.connect(self.nawt)
        self.clearnawtButton.clicked.connect(self.clearNawt)
        self.undoButton.clicked.connect(self.undo)

        app.aboutToQuit.connect(self.closeEvent)

        self.changeButtonState(False)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        if settings.get("lastPath") != "":
            self.openPath(settings.get("lastPath"))
        if settings.get("previousFile") != "":
            previousFile = settings.get("previousFile")

    def closeEvent(self):
        settings.set("previousFile", previousFile)
        settings.save()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.loadButton.setText(_translate("MainWindow", "Load Folder"))
        self.undoButton.setText(_translate("MainWindow", "↓Undo↑"))
        self.nawtButton.setText(_translate("MainWindow", "☒Nawt"))
        self.clearnawtButton.setText(_translate("MainWindow", "Delete"))
        self.hawtButton.setText(_translate("MainWindow", "❤Hawt"))
        self.label.setText(_translate("MainWindow", "No folder loaded"))
        # Hotkeys
        self.nawtButton.setShortcut(_translate("MainWindow", "Left"))
        self.hawtButton.setShortcut(_translate("MainWindow", "Right"))
        self.undoButton.setShortcut(_translate("MainWindow", "Down"))

    def openPath(self, path):
        global directory
        directory = path
        if not os.path.exists(directory + "/hawt"):
            os.makedirs(directory + "/hawt")
        if not os.path.exists(directory + "/nawt"):
            os.makedirs(directory + "/nawt")
        # print("CREATED FOLDERS")
        self.changeButtonState(True)
        self.loadNextImage(directory)

    def loadPath(self):
        global directory
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "Open Dir", "C:/")
        # print("CHOSEN DIR: " + directory)
        settings.set("lastPath", directory)
        settings.save()
        self.openPath(directory)
        return

    def updateCounts(self, directory):
        count = glob(directory + "/nawt/*.png")
        count.extend(glob(directory + '/nawt/*.jpg'))
        count.extend(glob(directory + '/nawt/*.jpeg'))
        self.nawtcount.setText("Nawt: " + str(len(count)))
        count = glob(directory + "/hawt/*.png")
        count.extend(glob(directory + '/hawt/*.jpg'))
        count.extend(glob(directory + '/hawt/*.jpeg'))
        self.hawtcount.setText("Hawt: " + str(len(count)))

    def clearNawt(self):
        global directory, previousFile
        if directory == "":
            return
        reply = QMessageBox.warning(QtWidgets.QWidget(), 'Are you sure?',
                                    'Are you sure you want to delete everything in the nawt-folder?\n THIS CANNOT BE UNDONE!',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for the_file in os.listdir(directory + "/nawt"):
                file_path = os.path.join(directory + "/nawt", the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    # elif os.path.isdir(file_path): shutil.rmtree(file_path)
                except Exception as e:
                    print(e)
            previousFile = ""
            self.updateCounts(directory)

    def loadNextImage(self, directory):
        global currentFile
        cwd = glob(directory + "/*.png")
        cwd.extend(glob(directory + '/*.jpg'))
        cwd.extend(glob(directory + '/*.jpeg'))
        self.totalcount.setText("Remaining: " + str(len(cwd)))
        self.updateCounts(directory)
        # print("CWD: " + str(cwd))
        if len(cwd) == 0:
            self.changeButtonState(False)
            self.label.setText("No more images. Choose new folder.")
            self.totalcount.setText("")
            settings.set("lastPath", "")
            settings.save()
            # print("ALL DONE!")
            self.clearNawt()
            return
        currentFile = cwd[0]

        # print("CWD: " + currentFile)
        # myPixmap = QtGui.QPixmap(currentFile)
        image_reader = QtGui.QImageReader()
        image_reader.setDecideFormatFromContent(True)
        image_reader.setFileName(currentFile)
        image = image_reader.read()
        myPixmap = QtGui.QPixmap.fromImage(image)
        image = None
        # print("Imageprofile created")
        myScaledPixmap = myPixmap.scaled(self.label.size(), QtCore.Qt.KeepAspectRatio)
        # print("Imageprofile scaled")
        self.label.setPixmap(myScaledPixmap)

    def hawt(self):
        global previousFile
        # print("hawt: " + currentFile + "   " + os.path.basename(currentFile))
        previousFile = directory + "/hawt/" + os.path.basename(currentFile)
        shutil.move(currentFile, directory + "/hawt/" + os.path.basename(currentFile))
        Path(directory + "/hawt/" + os.path.basename(currentFile)).touch(exist_ok=True)
        self.loadNextImage(directory)

    def nawt(self):
        global previousFile
        # print("nawt: " + currentFile + "   " + os.path.basename(currentFile))
        previousFile = directory + "/nawt/" + os.path.basename(currentFile)
        shutil.move(currentFile, directory + "/nawt/" + os.path.basename(currentFile))
        Path(directory + "/nawt/" + os.path.basename(currentFile)).touch(exist_ok=True)
        self.loadNextImage(directory)

    def undo(self):
        global previousFile
        if previousFile == "":
            QMessageBox.warning(QtWidgets.QWidget(), 'Not possible.',
                                'There is no previous file saved.',
                                QMessageBox.Ok, QMessageBox.Ok)
            return
        shutil.move(previousFile, directory + "/" + os.path.basename(previousFile))
        previousFile = ""
        self.loadNextImage(directory)

    def changeButtonState(self, val):
        self.hawtButton.setEnabled(val)
        self.nawtButton.setEnabled(val)
        self.clearnawtButton.setEnabled(val)
        self.undoButton.setEnabled(val)
        self.hawtButton.setVisible(val)
        self.nawtButton.setVisible(val)
        self.clearnawtButton.setVisible(val)
        self.undoButton.setVisible(val)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
