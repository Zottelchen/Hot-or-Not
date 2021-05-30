# -*- coding: utf-8 -*-

import ctypes
import os
import platform
import shutil
import sys
from glob import glob, escape

import magic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from easysettings import EasySettings
from natsort import os_sorted
from pathlib2 import Path

# MPV
os.environ["PATH"] = os.path.dirname(__file__) + os.pathsep + os.environ["PATH"]
import mpv

directory = ""
currentFile = ""
cwd = ""
previousFile = ""
previousDirectory = ""
myappid = u'hotornot'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
settings = EasySettings("hotornot.conf")
m = magic.Magic()


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
        MainWindow.setWindowTitle("Hot Or Not (Version 2.1)")
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
        self.notButton = QtWidgets.QPushButton(self.centralwidget)
        self.notButton.setGeometry(QtCore.QRect(0, 400, 100, 30))
        self.notButton.setStyleSheet("color: rgb(255, 147, 149);")
        self.notButton.setObjectName("notButton")
        self.clearnotButton = QtWidgets.QPushButton(self.centralwidget)
        self.clearnotButton.setGeometry(QtCore.QRect(0, 460, 100, 30))
        self.clearnotButton.setStyleSheet("color: rgb(255, 147, 149);")
        self.clearnotButton.setObjectName("notButton")
        self.hotButton = QtWidgets.QPushButton(self.centralwidget)
        self.hotButton.setGeometry(QtCore.QRect(1500, 400, 100, 30))
        self.hotButton.setStyleSheet("color: rgb(165, 213, 151)")
        self.hotButton.setObjectName("hotButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 0, 1380, 820))
        self.label.setStyleSheet("background-color: rgb(85, 85, 85);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        # gifcontainer
        self.container = QWidget(self.centralwidget)
        self.container.setAttribute(Qt.WA_DontCreateNativeAncestors)
        self.container.setAttribute(Qt.WA_NativeWindow)
        self.container.setGeometry(QtCore.QRect(110, 0, 1380, 820))
        self.container.setStyleSheet("background-color: rgb(85, 85, 85);")
        # self.container.setAlignment(QtCore.Qt.AlignCenter)
        self.player = mpv.MPV(wid=str(int(self.container.winId())),
                              log_handler=print,
                              player_operation_mode='pseudo-gui',
                              script_opts='osc-layout=box,osc-seekbarstyle=bar,osc-deadzonesize=0,osc-minmousemove=3',
                              input_default_bindings=True,
                              input_vo_keyboard=True, osc=True, loop='inf')
        self.container.setVisible(False)

        self.fileName = QtWidgets.QLabel(self.centralwidget)
        self.fileName.setGeometry(QtCore.QRect(990, 820, 500, 28))
        self.fileName.setStyleSheet("background-color: rgb(95, 95, 95);")
        self.fileName.setMargin(2)
        self.fileName.setAlignment(QtCore.Qt.AlignRight)
        self.fileName.setText("")
        self.openFileButton = QtWidgets.QPushButton(self.centralwidget)
        self.openFileButton.setGeometry(QtCore.QRect(1390, 850, 100, 30))
        self.openFileButton.setObjectName("openButton")
        MainWindow.setCentralWidget(self.centralwidget)
        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)

        self.totalcount = QtWidgets.QLabel(self.centralwidget)
        self.totalcount.setGeometry(730, 850, 200, 30)
        # self.count.setText("Count: xxx")

        self.hotcount = QtWidgets.QLabel(self.centralwidget)
        self.hotcount.setGeometry(QtCore.QRect(1500, 430, 100, 30))
        # self.hotcount.setText("Hot: xxx")
        self.notcount = QtWidgets.QLabel(self.centralwidget)
        self.notcount.setGeometry(QtCore.QRect(0, 430, 100, 30))
        # self.notcount.setText("Not: xxx")

        self.loadButton.clicked.connect(self.loadPath)
        self.hotButton.clicked.connect(self.hotclicked)
        self.notButton.clicked.connect(self.notclicked)
        self.clearnotButton.clicked.connect(self.clearNot)
        self.undoButton.clicked.connect(self.undo)
        if platform.system() == 'Windows':
            self.openFileButton.clicked.connect(self.openFile)
        else:
            self.openFileButton.setVisible(False)

        app.aboutToQuit.connect(self.closeEvent)

        self.changeButtonState(False)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        if settings.get("lastPath") != "":
            if os.path.exists(settings.get("lastPath")):
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
        self.notButton.setText(_translate("MainWindow", "☒Not"))
        self.clearnotButton.setText(_translate("MainWindow", "Delete"))
        self.hotButton.setText(_translate("MainWindow", "❤Hot"))
        self.label.setText(_translate("MainWindow", "No folder loaded"))
        self.openFileButton.setText(_translate("MainWindow", "Open file"))
        # Hotkeys
        self.notButton.setShortcut(_translate("MainWindow", "Left"))
        self.hotButton.setShortcut(_translate("MainWindow", "Right"))
        self.undoButton.setShortcut(_translate("MainWindow", "Down"))

    def openPath(self, path):
        global directory, previousDirectory, cwd
        directory = path
        if not os.path.exists(directory + "/hot"):
            os.makedirs(directory + "/hot")
        if not os.path.exists(directory + "/not"):
            os.makedirs(directory + "/not")
        # print("CREATED FOLDERS")
        # print(directory)
        cwd = glob(directory + "/*.png")
        cwd.extend(glob(directory + '/*.jpg'))
        cwd.extend(glob(directory + '/*.jpeg'))
        cwd.extend(glob(directory + '/*.gif'))
        cwd.extend(glob(directory + '/*.webm'))
        cwd.extend(glob(directory + '/*.mp4'))
        cwd = os_sorted(cwd)
        # print(cwd)
        self.changeButtonState(True)
        self.loadNextImage(directory)
        previousDirectory = os.path.dirname(directory)

    def loadPath(self):
        global directory
        if previousDirectory != "" and os.path.exists(previousDirectory):
            directory = QtWidgets.QFileDialog.getExistingDirectory(None, "Open Dir", previousDirectory)
        else:
            directory = QtWidgets.QFileDialog.getExistingDirectory(None, "Open Dir", "C:/")
        # print("CHOSEN DIR: " + directory)
        settings.set("lastPath", directory)
        settings.save()
        self.openPath(directory)
        return

    def updateCounts(self, directory):
        count = next(os.walk(directory + "/not/"))[2]
        self.notcount.setText("Not: " + str(len(count)))
        count = next(os.walk(directory + "/hot/"))[2]
        self.hotcount.setText("Hot: " + str(len(count)))
        self.totalcount.setText("Remaining: " + str(len(cwd)))

    def clearNot(self):
        global directory, previousFile
        if directory == "":
            return
        reply = QMessageBox.warning(QtWidgets.QWidget(), 'Are you sure?',
                                    'Are you sure you want to delete everything in the not-folder?\n THIS CANNOT BE UNDONE!',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for the_file in os.listdir(directory + "/not"):
                file_path = os.path.join(directory + "/not", the_file)
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
        self.updateCounts(directory)
        # print("CWD: " + str(cwd))
        if len(cwd) == 0:
            self.player.stop()
            self.container.setVisible(False)
            self.label.setVisible(True)
            self.changeButtonState(False)
            self.label.setText("No more images. Choose new folder.")
            self.totalcount.setText("")
            settings.set("lastPath", "")
            settings.save()
            # print("ALL DONE!")
            self.clearNot()
            os.startfile(directory)
            return
        currentFile = cwd[0]
        # print("CWD: " + currentFile)
        # myPixmap = QtGui.QPixmap(currentFile)
        image_reader = QtGui.QImageReader()
        image_reader.setDecideFormatFromContent(True)
        image_reader.setFileName(currentFile)
        self.fileName.setText(os.path.basename(currentFile))
        filetype = magic.from_file(currentFile, mime=True)
        if filetype in ('image/gif', 'video/webm', 'video/mp4'):  # todo: properly check if webm
            self.container.setVisible(True)
            self.label.setVisible(False)
            self.player.play(currentFile)
        elif filetype in ('image/png', 'image/jpg', 'image/jpeg'):
            self.player.stop()
            self.container.setVisible(False)
            self.label.setVisible(True)
            image = image_reader.read()
            myPixmap = QtGui.QPixmap.fromImage(image)
            # print("Imageprofile created")
            myScaledPixmap = myPixmap.scaled(self.label.size(), QtCore.Qt.KeepAspectRatio)
            # print("Imageprofile scaled")
            self.label.setPixmap(myScaledPixmap)

    def hotclicked(self):
        global previousFile, cwd
        self.player.stop()
        del cwd[0]
        # print("hot: " + currentFile + "   " + os.path.basename(currentFile))
        previousFile = directory + "/hot/" + os.path.basename(currentFile)
        shutil.move(currentFile, directory + "/hot/" + os.path.basename(currentFile))
        Path(directory + "/hot/" + os.path.basename(currentFile)).touch(exist_ok=True)
        self.loadNextImage(directory)

    def notclicked(self):
        global previousFile, cwd
        self.player.stop()
        del cwd[0]
        # print("not: " + currentFile + "   " + os.path.basename(currentFile))
        previousFile = directory + "/not/" + os.path.basename(currentFile)
        shutil.move(currentFile, directory + "/not/" + os.path.basename(currentFile))
        Path(directory + "/not/" + os.path.basename(currentFile)).touch(exist_ok=True)
        self.loadNextImage(directory)

    def undo(self):
        global previousFile, cwd
        if previousFile == "":
            QMessageBox.warning(QtWidgets.QWidget(), 'Not possible.',
                                'There is no previous file saved.',
                                QMessageBox.Ok, QMessageBox.Ok)
            return
        shutil.move(previousFile, directory + "/" + os.path.basename(previousFile))
        cwd.extend(glob(escape(directory + "/" + os.path.basename(previousFile))))
        cwd = sorted(cwd)
        previousFile = ""
        self.loadNextImage(directory)

    def changeButtonState(self, val, gif=False):
        self.hotButton.setEnabled(val)
        self.notButton.setEnabled(val)
        self.clearnotButton.setEnabled(val)
        self.undoButton.setEnabled(val)
        self.hotButton.setVisible(val)
        self.notButton.setVisible(val)
        self.clearnotButton.setVisible(val)
        self.undoButton.setVisible(val)
        if gif:
            self.loadButton.setVisible(val)
        if not val and not gif:
            self.notcount.setText("")
            self.hotcount.setText("")
            self.totalcount.setText("")
            self.fileName.setText("")

    def openFile(self):
        os.startfile(currentFile, 'open')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
