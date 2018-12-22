# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import cv2

class Ui_PhotoDialog():
    def setupUi(self, PhotoDialog, No_camera, cap):
        super().__init__() 
        PhotoDialog.setObjectName("PhotoDialog")
        self.Lable_video = QtWidgets.QLabel(PhotoDialog)
        self.Lable_video.setGeometry(QtCore.QRect(0, 0, 650, 490))
        # self.Lable_video.setText("-------------")
        self.Lable_video.setObjectName("Lable_video")
        
        self.timer_camera = QtCore.QTimer()
        self.cap = cap
        
        self.open_camera(No_camera)

        self.retranslateUi(PhotoDialog)
        QtCore.QMetaObject.connectSlotsByName(PhotoDialog)

    def retranslateUi(self, PhotoDialog):
        _translate = QtCore.QCoreApplication.translate
        PhotoDialog.setWindowTitle(_translate("PhotoDialog", "Camera"))
        PhotoDialog.setWindowFlags(PhotoDialog.windowFlags()|
                                   QtCore.Qt.WindowMinimizeButtonHint|
                                   QtCore.Qt.WindowSystemMenuHint)
        self.timer_camera.timeout.connect(self.show_camera)

    def open_camera(self, No_camera):
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(No_camera)
            if flag == False:
               QtWidgets.QMessageBox.warning(self, u"Warning", u"No Camera is detected", buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.Ok)
            else:
                self.timer_camera.start(30)


# Timer function
    def show_camera(self):
        flag, self.image = self.cap.read()
        # cv2.putText(self.image,'OpenCV',(10,10), cv2.FONT_HERSHEY_PLAIN, 2,(255,255,255),1,cv2.LINE_AA)
        show = cv2.resize(self.image, (640, 480))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.Lable_video.setPixmap(QtGui.QPixmap.fromImage(showImage))