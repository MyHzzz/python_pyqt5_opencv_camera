from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QGraphicsRectItem, QGraphicsScene, QMessageBox, QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from video_box import VideoBox
from photo_box import PhotoBox
import cv2
import sys
from socket import *
from settings import *
import MainInterface
import PhotoDialog
import VideoDialog
import time

class MainProgram(QWidget,MainInterface.Ui_TabWidget):
   
   def __init__(self):
      super().__init__()
      self.setupUi(self)
      self.ADDR = ADDR
      # self.connect_Socket()  
      self.camera_flag = 0
      self.savepath = ""
      self.filename_camera = ""
      self.action_connect()

   def connect_Socket(self):
      #创建数据报套接字
      self.sockfd = socket(AF_INET,SOCK_DGRAM) 
      
   def action_connect(self):
      #拍照的信号与槽
      self.Button_camera2.clicked.connect(self.Button_camera_clicked2) 
      self.Button_filename2.clicked.connect(self.Button_filename_clicked2)
      self.Button_savepath2.clicked.connect(self.Button_savepath_clicked2)
      self.Button_recording2.clicked.connect(self.Button_recording_clicked2)
      self.Button_endrecording2.clicked.connect(self.Button_endrecording_clicked2)
      #短视频的信号与槽
      self.Button_camera.clicked.connect(self.Button_camera_clicked) 
      self.Button_filename.clicked.connect(self.Button_filename_clicked)
      self.Button_savepath.clicked.connect(self.Button_savepath_clicked)
      self.Button_recording.clicked.connect(self.Button_recording_clicked)
      self.Button_endrecording.clicked.connect(self.Button_endrecording_clicked)
      #查看视频的信号与槽
      self.Button_videopath.clicked.connect(self.Button_videopath_clicked)
      self.Button_videoview.clicked.connect(self.Button_videoview_clicked)
      #查看照片的信号与槽
      self.Button_photopath.clicked.connect(self.Button_photopath_clicked)
      self.Button_photoview.clicked.connect(self.Button_photoview_clicked)

      #注册登录
      self.btnLogin.clicked.connect(self.Button_login_clicked)
      self.btnSignin.clicked.connect(self.Button_signin_clicked)
      #重置
      self.btnLoginreset.clicked.connect(self.Button_loginreset_clicked)
      self.btnSignreset.clicked.connect(self.Button_signinreset_clicked)
   # 拍照功能
   def Button_camera_clicked2(self):
      if self.camera_flag == 0:
         self.cap1 = cv2.VideoCapture(0)
         if self.cap1.isOpened() == True:
            self.sub_ui1 = PhotoDialog.Ui_PhotoDialog()
            self.Dialog1 = QtWidgets.QDialog()
            
            self.sub_ui1.setupUi(self.Dialog1, 0, self.cap1)
            self.Dialog1.show()
            
            self.camera_flag = 1
            self.Dialog1.exec()
            if self.sub_ui1.cap.isOpened():
               self.sub_ui1.cap.release()
            if self.sub_ui1.timer_camera.isActive():
               self.sub_ui1.timer_camera.stop()
               self.camera_flag = 0
         else:
            self.cap1.release()
            QMessageBox.information(self, "Info", "Camera is Null", QMessageBox.Yes | QMessageBox.No)
      # if self.camera_flag == 0:
      #    self.cap1 = cv2.VideoCapture(0)
      #    if self.cap1.isOpened() == True:
      #          self.sub_ui1 = PhotoDialog.Ui_PhotoDialog()
      #          # self.sub_ui1.setupUi()
      #          self.sub_ui1.show()
      #          self.camera_flag = 1
      #          # self.sub_ui1.exec()
      #          if self.sub_ui1.cap.isOpened():
      #             self.sub_ui1.cap.release()
      #          if self.sub_ui1.timer_camera.isActive():
      #             self.sub_ui1.timer_camera.stop()
      #             self.camera_flag = 0

   # 文件名
   def Button_filename_clicked2(self):
      # self.filename_camera = ''
      base_filename = self.Edit_filename2.text()
      if base_filename == "":
         base_filename = "Photo"
      self.filename_camera = ''.join((base_filename, "_"))
      print("filename_camera:",self.filename_camera)

   def Button_savepath_clicked2(self):
      self.savepath = QFileDialog.getExistingDirectory(self, "Choose the path", './PHOTOS/')
      self.savepath = ''.join((self.savepath, "/"))
      self.Label_savepath2.setText(self.savepath)
      self.filename_camera = ''.join((self.savepath, self.filename_camera))

   def Button_recording_clicked2(self):
      if self.filename_camera == "":
         self.filename_camera = ''.join(("Photo", "_"))
      if self.savepath == "":
         self.savepath = "./PHOTOS/"
         self.filename_camera = ''.join((self.savepath, self.filename_camera))
      t=list(time.localtime()[0:6])
      t_str = [str(i) for i in t]
      t_str = ''.join(t_str)
      if hasattr(self, 'sub_ui1'):
         savename_camera = ''.join((self.filename_camera, t_str, '.jpg'))
         ret ,frame = self.sub_ui1.cap.read()
         cv2.imwrite(savename_camera,frame)
         self.sub_ui1.timer_camera.stop()
         self.Label_mrecordingtime2.setText("已保存")
      self.Button_recording2.setEnabled(False)
      print("self.filename_camera",self.filename_camera)
      print("savename_camera",savename_camera)
      self.filename_camera = ""
      self.savepath = ""

      
   def Button_endrecording_clicked2(self):
      self.Label_mrecordingtime2.setText("")
      self.sub_ui1.timer_camera.start(30)
      self.Button_recording2.setEnabled(True)
      self.Edit_filename2.setText("")
      self.Label_savepath2.setText("")

   #短视频
   def Button_camera_clicked(self):

      self.filename_camera = ''
      if self.camera_flag == 0:
         # self.cap1 = cv2.VideoCapture("./VIDEOS/TEST1_camera1_1137584.avi")
         self.cap1 = cv2.VideoCapture(0)
         if self.cap1.isOpened() == True:
            self.sub_ui1 = VideoDialog.Ui_VideoDialog()
            self.Dialog1 = QtWidgets.QDialog()
         
            self.sub_ui1.setupUi(self.Dialog1, 0, self.cap1)
            self.Dialog1.show()
            
            self.camera_flag = 1
            self.Dialog1.exec()
            if self.sub_ui1.cap.isOpened():
               self.sub_ui1.cap.release()
            if self.sub_ui1.timer_camera.isActive():
               self.sub_ui1.timer_camera.stop()
               self.camera_flag = 0
         else:
            self.cap1.release()
            QMessageBox.information(self, "Info", "Camera is Null", QMessageBox.Yes | QMessageBox.No)
   # 文件名
   def Button_filename_clicked(self):
      base_filename = self.Edit_filename.text()
      if base_filename == "":
         base_filename = "Video"
      self.filename_camera = ''.join((base_filename, "_"))
      print("filename_camera:",self.filename_camera)

   def Button_savepath_clicked(self):
      self.savepath = QFileDialog.getExistingDirectory(self, "Choose the path", './VIDEOS/')
      self.savepath = ''.join((self.savepath, "/"))
      self.Label_savepath.setText(self.savepath)
      self.filename_camera = ''.join((self.savepath, self.filename_camera))

   def Button_recording_clicked(self):
      if self.filename_camera == "":
         self.filename_camera = ''.join(("Video", "_"))
      if self.savepath == "":
         self.savepath = "./VIDEOS/"
         self.filename_camera = ''.join((self.savepath, self.filename_camera))
      t=list(time.localtime()[0:6])
      t_str = [str(i) for i in t]
      t_str = ''.join(t_str)
      if hasattr(self, 'sub_ui1'):
         savename_camera = ''.join((self.filename_camera, t_str, '.avi'))
         fourcc = cv2.VideoWriter_fourcc(*'XVID')
         self.sub_ui1.out = cv2.VideoWriter(savename_camera,fourcc, 30.0, (640,480))
         self.sub_ui1.record_flag = 1
         self.Label_mrecordingtime.setText("Recording")
      self.Button_recording.setEnabled(False)
      print("self.filename_camera",self.filename_camera)
      print("savename_camera",savename_camera)
      self.filename_camera = ""
      self.savepath = ""
      
   def Button_endrecording_clicked(self):
      self.Label_mrecordingtime.setText("")
      if hasattr(self, 'sub_ui1'):
         if self.sub_ui1.record_flag == 1:
            self.sub_ui1.record_flag = 0
            self.sub_ui1.out.release()
            print("clock:",time.clock())
      self.Button_recording.setEnabled(True)
      self.Edit_filename.setText("")
      self.Label_savepath.setText("")

   #查看视频与照片
   def Button_videopath_clicked(self):
      self.videoName,self.videoType= QFileDialog.getOpenFileName(self, #返回路径下视频的全名称==
                                 "打开视频",
                                 "",
                                 " *.mp4;;*.avi;;All Files (*)")
      self.Label_videopath.setText(self.videoName)
   def Button_videoview_clicked(self):
      self.mw = VideoBox()
      self.mw.set_video(self.videoName, VideoBox.VIDEO_TYPE_OFFLINE, False)
      self.mw.show()
      self.Label_videopath.setText("")
   def Button_photopath_clicked(self):
      self.imgName,self.imgType= QFileDialog.getOpenFileName(self,
                                 "打开图片",
                                 "",
                                 " *.jpg;;*.png;;*.jpeg;;*.bmp;;All Files (*)")
      self.Label_photopath.setText(self.imgName)
   def Button_photoview_clicked(self):
      self.pv = PhotoBox(self.imgName)
      self.pv.show()
      self.Label_photopath.setText("")
   #登录功能
   def Button_login_clicked(self):
      name = self.username.text()
      passwd = self.password.text()
      checkpasswd = self.checkpsw.text()
      if name == '':
         replay = QMessageBox.warning(self, "warning", "账号不准为空", QMessageBox.Yes)
      elif passwd == '':
         replay = QMessageBox.warning(self, "warning", "密码不能为空", QMessageBox.Yes)
      elif passwd != checkpasswd:
         replay = QMessageBox.warning(self, "warning", "两次密码不一致", QMessageBox.Yes)
      
      else:
         msg = "L %s %s"%(name,passwd)
         #创建数据报套接字函数
         self.connect_Socket()
         #向服务端发送消息
         self.sockfd.sendto(msg.encode(),ADDR)
         data,addr = self.sockfd.recvfrom(1024)
         # print(data)
         if data.decode() == 'OK':
            replay = QMessageBox.information(self, "提示", "登录成功,欢迎您,%s"%name, QMessageBox.Yes)
         else:
            replay = QMessageBox.information(self,"提示","登录失败，请检查账号密码是否正确",QMessageBox.Yes)
   def Button_loginreset_clicked(self):
      self.username.setText("")
      self.password.setText("")
      self.checkpsw.setText("")
   def Button_signin_clicked(self):
      newname = self.newname.text()
      newpasswd = self.newpasswd.text()
      checkpasswd = self.checknewpasswd.text()
      if (' ' in newname) or (' ' in newpasswd):
         replay = QMessageBox.warning(self, "warning", "账号或者密码不能有空格", QMessageBox.Yes)
      elif newpasswd == "":
         replay = QMessageBox.warning(self, "warning", "密码不能为空", QMessageBox.Yes)
      elif newpasswd != checkpasswd:
         replay = QMessageBox.warning(self, "warning", "两次密码输入不一致", QMessageBox.Yes)
      else:
         msg = 'R %s %s'%(newname,newpasswd)
         #创建套接字
         self.connect_Socket()
         #发送请求
         self.sockfd.sendto(msg.encode(),ADDR)

         #等待回复
         data,addr = self.sockfd.recvfrom(1024)
         # print(data)
         data = data.decode()
         if data == 'OK':
            replay = QMessageBox.information(self,"提示","注册成功，欢迎%s的加入"%newname,QMessageBox.Yes)

         elif data == 'EXISTS':
            replay = QMessageBox.information(self,"提示","该用户已存在，请重新申请",QMessageBox.Yes)

         elif data == 'FALL':
            print("FALL")
            replay = QMessageBox.information(self,"提示","注册失败",QMessageBox.Yes)      
   def Button_signinreset_clicked(self):
      self.newname.setText("")
      self.newpasswd.setText("")
      self.checknewpasswd.setText("")



      




      

       
