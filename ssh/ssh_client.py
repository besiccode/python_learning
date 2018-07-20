
from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os, socket

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(705, 377)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(43, 18, 641, 240))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_1 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_1.setGeometry(QtCore.QRect(42, 280, 371, 34))
        self.textEdit_1.setObjectName("textEdit_1")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(430,288,80,32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_1.setGeometry(QtCore.QRect(505, 288, 82, 32))
        self.pushButton_1.setObjectName("pushButton_1")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 705, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ssh"))
        self.pushButton.setText(_translate("MainWindow", "send"))
        self.pushButton_1.setText(_translate("MainWindow", "exit"))


class socKet():
    def __init__(self):
        super().__init__()
        self.mainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.mainWindow)
        self.ui.textEdit_1.setFont(QtGui.QFont("Roman times", 18, QtGui.QFont.Bold))
        self.ui.textEdit.setFont(QtGui.QFont("Roman times", 15, QtGui.QFont.Bold))
        self.ui.pushButton.clicked.connect(self.send)
        self.ui.pushButton_1.clicked.connect(self.end)
        self.client = socket.socket()
        self.client.connect(("118.89.32.173", 13597))
        self.ui.textEdit.setReadOnly(True)

    def show(self):
        self.mainWindow.show()


    def send(self):
        data = self.ui.textEdit_1.toPlainText()
        self.ui.textEdit_1.setText("")
        if data == "quit":
            self.client.send(data.encode("utf-8"))
            self.client.close()
            return
        self.client.send(data.encode("utf-8"))
        data = self.client.recv(30000)
        self.ui.textEdit.setTextColor(QtCore.Qt.green)
        self.ui.textEdit.append(data.decode())


    def end(self):
        data = "quit"
        self.client.send(data.encode("utf-8"))
        self.client.close()
        sys.exit()





app = QtWidgets.QApplication(sys.argv)
a = socKet()
a.show()
sys.exit(app.exec())