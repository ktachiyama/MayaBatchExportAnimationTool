'''
Krysten Tachiyama
Week 4: Create a UI tool that applies a given animation
        onto a given character and saves the file via Python
'''

from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI  # needed to grab main Maya pointer
from BatchExportAnimation import *


def getMayaWindow():

    mayaWindowPtr = maya.OpenMayaUI.MQtUtil.mainWindow()

    # converts a pointer to  a long and then
    # creates an instance of it that's a QWidget
    return wrapInstance(long(mayaWindowPtr), QtWidgets.QWidget)


class BatchAnimationsDialog(QtWidgets.QDialog):

    def __init__(self):

        mayaMain = getMayaWindow()
        super(BatchAnimationsDialog, self).__init__(mayaMain)

        self.setWindowTitle("Apply Animation Onto Character")
        self.setMinimumWidth(1000)
        self.setMinimumHeight(400)

        self.createWidgets()
        self.createLayouts()
        # self.replaceText()
        self.createConnections()

    def createWidgets(self):
        # get character file
        self.charFileText = QtWidgets.QLabel()
        self.charFileText.setText("Character File Directory")

        self.charFileInput = QtWidgets.QLineEdit()
        self.charFileInputBtn = QtWidgets.QPushButton()
        self.charFileInputBtn.setIcon(QtGui.QIcon(":fileOpen.png"))

        # get animation file
        self.animFileText = QtWidgets.QLabel()
        self.animFileText.setText("Animation File Directory")

        self.animFileInput = QtWidgets.QLineEdit()
        self.animFileInputBtn = QtWidgets.QPushButton()
        self.animFileInputBtn.setIcon(QtGui.QIcon(":fileOpen.png"))

        # get path where file will be saved
        self.saveFileText = QtWidgets.QLabel()
        self.saveFileText.setText("Save File Path")

        self.saveFileInput = QtWidgets.QLineEdit()
        self.saveFileInputBtn = QtWidgets.QPushButton()
        self.saveFileInputBtn.setIcon(QtGui.QIcon(":fileOpen.png"))

        # create button
        self.batchBtn = QtWidgets.QPushButton("Batch")

    def createLayouts(self):
        self.mainLayout = QtWidgets.QVBoxLayout(self)

        self.charLayout = QtWidgets.QHBoxLayout(self)
        self.charLayout.addWidget(self.charFileText)
        self.charLayout.addWidget(self.charFileInput)
        self.charLayout.addWidget(self.charFileInputBtn)

        self.animLayout = QtWidgets.QHBoxLayout(self)
        self.animLayout.addWidget(self.animFileText)
        self.animLayout.addWidget(self.animFileInput)
        self.animLayout.addWidget(self.animFileInputBtn)

        self.saveLayout = QtWidgets.QHBoxLayout(self)
        self.saveLayout.addWidget(self.saveFileText)
        self.saveLayout.addWidget(self.saveFileInput)
        self.saveLayout.addWidget(self.saveFileInputBtn)

        self.btnLayout = QtWidgets.QHBoxLayout(self)
        self.btnLayout.addWidget(self.batchBtn)

        self.mainLayout.addLayout(self.charLayout)
        self.mainLayout.addLayout(self.animLayout)
        self.mainLayout.addLayout(self.saveLayout)
        self.mainLayout.addLayout(self.btnLayout)

    def browseAnimDir(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self)[0]
        if path:
            self.animFileInput.setText(path)

    def browseCharDir(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self)[0]
        if path:
            self.charFileInput.setText(path)

    def browseSavePath(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self)
        if path:
            self.saveFileInput.setText(path)

    def getSaveDir(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self)
        if directory:
            #path = directory + '\/' + fileName + '/.mb'
            # self.saveFileInput.setText(path)
            self.saveFileInput.setText(directory + '/' + 'wk04_homework.mb')
            # print(self.saveFileInput)

    def batchAnimation(self):
        charDir = self.charFileInput.text()
        animDir = self.animFileInput.text()
        saveDir = self.saveFileInput.text()

        BatchExportAnimation.batchAnimations(charDir, animDir, saveDir)

    def createConnections(self):
        self.charFileInputBtn.clicked.connect(self.browseCharDir)
        self.animFileInputBtn.clicked.connect(self.browseAnimDir)
        # self.saveFileInputBtn.clicked.connect(self.browseSavePath)
        # self.saveFileInputBtn.clicked.connect(self.getSaveDir("homework_wk04"))
        self.saveFileInputBtn.clicked.connect(self.getSaveDir)

        self.batchBtn.clicked.connect(self.batchAnimation)


try:
    dialog.close()
    dialog.deleteLater()
except:
    pass

dialog = BatchAnimationsDialog()
dialog.show()
