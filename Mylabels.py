from ntpath import join
import PyQt5
from PyQt5.QtWidgets import QAction, QMenu, QMessageBox, QWidget,QApplication,QLabel
from PyQt5.QtCore import QEasingCurve, QRect,Qt
from PyQt5.QtGui import QColor, QCursor, QGradient, QImage,QPixmap,QPainter,QPen,QGuiApplication
import cv2
import sys

class MyLabel(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False
    hasScaled = False

    def mousePressEvent(self,event):
        if event.buttons() == Qt.LeftButton:
            self.flag = True
            self.x0 = event.x()
            self.y0 = event.y()
        
    def wheelEvent(self,event):
        try:
            pix = self.pixmap()
            angle = event.angleDelta() /8
            '''self.setPixmap(self.pixmap().scaled(pix.width()+angle.y(),\
                    (pix.height()*(pix.width()+angle.y()))/ pix.width()))'''
            self.setPixmap(self.pixmap().scaled(pix.width()+angle.y(),\
                    pix.height()+angle.y())) 
            self.hasScaled = True       
        except:
            pass
    
    def contextMenuEvent(self,ev):
        menu = QMenu(self)
        open_action=QAction("截图",menu)
        open_action.triggered.connect(self.cutImg)
        menu.addAction(open_action)
        open_action=QAction("取消",menu)
        open_action.triggered.connect(self.cancel)
        menu.addAction(open_action)
        menu.exec_(ev.globalPos())

    def cutImg(self):
        pix = self.pixmap()
        try:
            pix_cut = pix.copy(self.rect)
            self.setPixmap(pix_cut)
        except:
            QMessageBox.information(self,"提醒","未选中图片")

    def cancel(self):
        self.update()
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
    def mouseReleaseEvent(self,event):
        self.flag = False
    
    def mouseMoveEvent(self,event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()
    
    def paintEvent(self, event):
        super().paintEvent(event)
        #self.rects = [self.x0,self.y0,self.x1,self.y1]
        if self.x1>self.x0 and self.y1>self.y0:
            self.rect = QRect(self.x0,self.y0,abs(self.x1-self.x0),abs(self.y1-self.y0))
            painter = QPainter(self)
            blue = QColor(0,0,255)
            painter.setPen(QPen(blue))
            painter.drawRect(self.rect)
        elif self.x0>self.x1 and self.y1>self.y0:
            self.rect = QRect(self.x1,self.y0,abs(self.x0-self.x1),abs(self.y1-self.y0))
            painter = QPainter(self)
            blue = QColor(0,0,255)
            painter.setPen(QPen(blue))
            painter.drawRect(self.rect)
        elif self.x1>self.x0 and self.y0>self.y1:
            self.rect = QRect(self.x0,self.y1,abs(self.x1-self.x0),abs(self.y0-self.y1))
            painter = QPainter(self)
            blue = QColor(0,0,255)
            painter.setPen(QPen(blue))
            painter.drawRect(self.rect)  
        elif self.x0>self.x1 and self.y0>self.y1:
            self.rect = QRect(self.x1,self.y1,abs(self.x0-self.x1),abs(self.y0-self.y1))
            painter = QPainter(self)
            blue = QColor(0,0,255)
            painter.setPen(QPen(blue))
            painter.drawRect(self.rect)   

    def getRect(self):
        return self.rect