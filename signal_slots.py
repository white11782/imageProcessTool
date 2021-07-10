from os import spawnve
from PyQt5 import QtWidgets,QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import QDir, QModelIndex, QStringListModel,Qt
from cv2 import data
from numpy.core.fromnumeric import shape
from  Ui_main import Ui_MainWindow
from PyQt5.QtWidgets import QAbstractItemView, QFileDialog,QMessageBox, QSlider
from PyQt5.QtGui import QImage, QPalette,QBrush,QPixmap
import cv2
import numpy as np
import threading
from Mylabels import MyLabel

class  MyWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.setupUi(self)
        self.label = MyLabel(self.tab)
        self.label.setText("")
        self.label.setObjectName("label")
        self.label.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = MyLabel(self.tab_2)
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_2.setAlignment(Qt.AlignCenter)
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        #多线程
        self.threads = []
        self.action_4.triggered.connect(self.openImg)
        self.ls = []
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.processingImg = ""
        self.action.triggered.connect(self.gray)
        self.action_6.triggered.connect(self.binary)
        self.action_5.triggered.connect(self.openFiles)
        self.listView.clicked.connect(self.clicked)  
        self.slider = QtWidgets.QSlider(self.label_2)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setEnabled(False)
        self.slider.setVisible(False)
        #self.spinBox = QtWidgets.QAbstractSpinBox(self.tab_2)
        #self.spinBox.setVisible(False)
        self.actionbaocun.triggered.connect(self.saveFile)
        self.actionfanzhuanyanse.triggered.connect(self.reverseThread)
        self.actionfanzhuanyanse.setEnabled(False)
        self.action_2.triggered.connect(self.cutImg)

    def openImg(self):
        file,ok = QtWidgets.QFileDialog.getOpenFileName(self,"打开","./","All Files(*)")
        if file not in self.ls:
            self.ls.append(file)
        slm = QStringListModel()
        slm.setStringList(self.ls)
        self.listView.setModel(slm)

    def openFiles(self):
        mFolderPath = QtWidgets.QFileDialog.getExistingDirectory(None,"Open Folder","./")
        dir = QDir(mFolderPath)
        #dir.setNameFilters("All Files(*)")
        mImgNames = dir.entryList()
        for i in range(len(mImgNames)):
            if mImgNames[i] not in self.ls:
                self.ls.append(mFolderPath+"/"+mImgNames[i])
        slm = QStringListModel()
        slm.setStringList(self.ls)
        self.listView.setModel(slm)
        '''for i in range(len(mImgNames)):
            if mImgNames[i] not in self.ls:
                self.ls.pop()'''
    
    def saveFile(self):
        filePath,ok = QFileDialog.getSaveFileName(self,"save","./","bmp(*.bmp);;png(*.png);;all files(*.*)")
        if filePath is not None and ok:
            cv2.imwrite(filePath,self.savMat)

    def clicked(self,qModelIndex):
        pix = QPixmap(self.ls[qModelIndex.row()])
        #self.label.setPixmap(pix.scaled(self.label.width(),self.label.height()))
        if pix.width()>self.label.width() and pix.height()>self.label.height():
            self.label.setPixmap(pix.scaled(self.label.height()*pix.width()/pix.height()\
                ,self.label.height()))
        elif pix.width()<self.label.width() and pix.height()<self.label.height():
            self.label.setPixmap(pix)
        elif pix.width()>self.label.width() and pix.height()<self.label.height():
            self.label.setPixmap(pix.scaled(self.label.width(),self.label.width()*pix.height/pix.width()))
        elif pix.width()<self.label.width() and pix.height()>self.label.height():
            self.label.setPixmap(pix.scaled(pix.width()*self.label.height()/pix.height(),\
                pix.height()))
        self.processingImg = self.ls[qModelIndex.row()]
        img = cv2.imread(self.processingImg,cv2.IMREAD_ANYCOLOR)
        if img is None:
            self.statusbar.showMessage("未选中图片")  
        elif len(img.shape) == 3:
            self.statusbar.showMessage(self.processingImg+"：图片为三通道图"+str(img.shape))
        elif len(img.shape) == 2:
            self.statusbar.showMessage(self.processingImg+"：图片为单通道图"+str(img.shape))
    def gray(self):
        self.slider.setEnabled(False)
        self.slider.setVisible(False)
        self.actionfanzhuanyanse.setEnabled(False)
        self.label_2.clear()
        img = cv2.imread(self.processingImg,cv2.IMREAD_ANYCOLOR)
        #在这加一个是否为灰度图的判断
        if img is None:
            QMessageBox.information(self,"注意","请确认已经选中图片！")
            return
        elif len(img.shape) == 3:
            imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        else:
            imgGray = img
        pix_gray = QPixmap(self.mat2qimg(imgGray))
        #self.label_2.setPixmap(pix_gray.scaled(self.label_2.width(),self.label_2.height()))
        if pix_gray.width()>self.label_2.width() and pix_gray.height()>self.label_2.height():
            self.label_2.setPixmap(pix_gray.scaled(self.label_2.height()*pix_gray.width()/pix_gray.height()\
                ,self.label_2.height()))
        elif pix_gray.width()<self.label_2.width() and pix_gray.height()<self.label_2.height():
            self.label_2.setPixmap(pix_gray)
        elif pix_gray.width()>self.label_2.width() and pix_gray.height()<self.label_2.height():
            self.label_2.setPixmap(pix_gray.scaled(self.label_2.width(),self.label_2.width()*pix_gray.height/pix_gray.width()))
        elif pix_gray.width()<self.label_2.width() and pix_gray.height()>self.label.height():
            self.label_2.setPixmap(pix_gray.scaled(pix_gray.width()*self.label_2.height()/pix_gray.height(),\
                pix_gray.height()))
        self.savMat = imgGray

    def binary(self):
        self.slider.setEnabled(True)
        self.slider.setVisible(True)
        self.actionfanzhuanyanse.setEnabled(True)
        img = cv2.imread(self.processingImg,cv2.IMREAD_GRAYSCALE)
        if img is None:
            QMessageBox.information(self,"注意","请确认已经选中图片！")
            return
        _,thre= cv2.threshold(img,self.slider.value(),255,cv2.THRESH_BINARY)
        pix_thre = QPixmap(self.mat2qimg(thre))
        self.savMat = thre
        self.label_2.setPixmap(pix_thre.scaled(self.label_2.width(),self.label_2.height()))
        self.slider.valueChanged.connect(self.valChanged)
        self.slider.setMaximum(255)
        self.slider.setMinimum(0)
        self.slider.setSingleStep(1)
        
    def valChanged(self):
        img = cv2.imread(self.processingImg)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        _,thre = cv2.threshold(img,self.slider.value(),255,cv2.THRESH_BINARY)
        self.savMat = thre
        pix_thre = QPixmap(self.mat2qimg(thre))
        if pix_thre.width()>self.label_2.width() and pix_thre.height()>self.label_2.height():
            self.label_2.setPixmap(pix_thre.scaled(self.label_2.height()*pix_thre.width()/pix_thre.height()\
                ,self.label_2.height()))
        elif pix_thre.width()<self.label_2.width() and pix_thre.height()<self.label_2.height():
            self.label_2.setPixmap(pix_thre)
        elif pix_thre.width()>self.label_2.width() and pix_thre.height()<self.label_2.height():
            self.label_2.setPixmap(pix_thre.scaled(self.label_2.width(),self.label_2.width()*pix_thre.height/pix_thre.width()))
        elif pix_thre.width()<self.label_2.width() and pix_thre.height()>self.label.height():
            self.label_2.setPixmap(pix_thre.scaled(pix_thre.width()*self.label_2.height()/pix_thre.height(),\
                pix_thre.height()))
        #self.label_2.setPixmap(pix_thre.scaled(self.label_2.width(),self.label_2.height()))
    
    def mat2qimg(self,mat):
        img = QImage()
        if len(mat.shape) == 3:
            mat = cv2.cvtColor(mat,cv2.COLOR_BGR2RGB)
                #img = QImage(mat.shape[0],mat.shape[1],QImage.Format_RGB888)
            img = QImage(mat.data,mat.shape[1],mat.shape[0],3*mat.shape[1],QImage.Format_RGB888)
            return img
        elif len(mat.shape) == 2:
            img = QImage(mat.data,mat.shape[1],mat.shape[0],mat.shape[1],QImage.Format_Indexed8)
            return img
    
    def reverse(self):
        for i in range(self.savMat.shape[0]):
            for j in range(self.savMat.shape[1]):
                if self.savMat[i,j] == 0:
                    self.savMat[i,j] = 255
                else:
                    self.savMat[i,j] = 0
        #self.progresReverse = QtWidgets.QProgressBar(self.statusBar)
        reverImg = QPixmap(self.mat2qimg(self.savMat))
        #图片比例设置正确，加一个判断条件                                                                             
        if reverImg.width()>self.label_2.width() and reverImg.height()>self.label_2.height():
            self.label_2.setPixmap(reverImg.scaled(self.label_2.height()*reverImg.width()/reverImg.height()\
                ,self.label_2.height()))
        elif reverImg.width()<self.label_2.width() and reverImg.height()<self.label_2.height():
            self.label_2.setPixmap(reverImg)
        elif reverImg.width()>self.label_2.width() and reverImg.height()<self.label_2.height():
            self.label_2.setPixmap(reverImg.scaled(self.label_2.width(),self.label_2.width()*reverImg.height/reverImg.width()))
        elif reverImg.width()<self.label_2.width() and reverImg.height()>self.label.height():
            self.label_2.setPixmap(reverImg.scaled(reverImg.width()*self.label_2.height()/reverImg.height(),\
                reverImg.height()))

    def reverseThread(self):
        t = threading.Thread(target=self.reverse)
        self.threads.append(t)
        #t.daemon = True 设置守护线程：退出主程序该线程也退出，False主程序退出该线程不退出
        t.start()

    def cutImg(self): 
        pass