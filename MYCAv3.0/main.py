from PyQt5 import QtCore, QtGui, QtWidgets
from MainProgram import MainProgram
import sys
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainProgram()
    mainWindow.show()
    sys.exit(app.exec_())
