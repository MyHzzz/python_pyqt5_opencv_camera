from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QGraphicsRectItem, QGraphicsScene, QMessageBox, QMainWindow
from PyQt5.QtGui import QPixmap
import sys
class PhotoBox(QWidget):
    def __init__(self,photo_url):
        # print(photo_url)
        super().__init__()
        # print("---")
        lb1 = QLabel(self)
        pix = QPixmap(photo_url).scaled(self.width(), self.height())

        lb1.setGeometry(0,0,self.width(), self.height())
        lb1.setStyleSheet("border: 2px solid red")
        lb1.setPixmap(pix)
if __name__ == "__main__":
    mapp = QApplication(sys.argv)
    mw = PhotoBox('./PHOTOS/cat.jpeg')
    mw.show()
    sys.exit(mapp.exec_())
    