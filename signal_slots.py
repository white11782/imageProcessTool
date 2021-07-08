from PyQt5 import QtWidgets,QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import QDir, QModelIndex, QStringListModel
from  Ui_main import Ui_MainWindow
from PyQt5.QtWidgets import QAbstractItemView, QFileDialog,QMessageBox, QSlider
from PyQt5.QtGui import QImage, QPalette,QBrush,QPixmap
import cv2


'''
图片显示的转换弄完
'''
class  MyWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.setupUi(self)
        self.action_4.triggered.connect(self.openImg)
        self.ls = []
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.processingImg = ""
        self.action.triggered.connect(self.gray)
        self.action_6.triggered.connect(self.binary)
        self.action_5.triggered.connect(self.openFiles)
        self.listView.clicked.connect(self.clicked)

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

    def clicked(self,qModelIndex):
        pix = QPixmap(self.ls[qModelIndex.row()])
        self.label.setPixmap(pix)
        self.processingImg = self.ls[qModelIndex.row()]

    def gray(self):
        self.label_2.clear()
        img = cv2.imread(self.processingImg)
        imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        cv2.imwrite("imgGray.jpg",imgGray)
        pix_gray = QPixmap("imgGray.jpg")
        self.label_2.setPixmap(pix_gray)

    def binary(self):
        self.slider = QtWidgets.QSlider(self.tab_2)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        img = cv2.imread(self.processingImg)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        _,thre = cv2.threshold(img,self.slider.value(),255,cv2.THRESH_BINARY)
        pix_thre = QPixmap(self.mat2qimg(thre))
        self.label_2.setPixmap(pix_thre)
        self.slider.valueChanged.connect(self.valChanged)
        self.slider.setMaximum(255)
        self.slider.setMinimum(0)
        self.slider.setSingleStep(1)
    
    def valChanged(self):
        img = cv2.imread(self.processingImg)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        _,thre = cv2.threshold(img,self.slider.value(),255,cv2.THRESH_BINARY)
        pix_thre = QPixmap(self.mat2qimg(thre))
        self.label_2.setPixmap(pix_thre)
    
    def mat2qimg(self,mat):
        img = QImage()
        if (len(mat.shape) == 3):
            mat = cv2.cvtColor(mat,cv2.COLOR_BGR2RGB)
            img = QImage(mat.shape[1],mat.shape[0],QImage.Format_RGB888)
        else:
            img = QImage(mat.shape[0],mat.shape[1],QImage.Format_Indexed8)
        return img