
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(931, 616)
        Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Form.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(-10, 20, 771, 551))
        self.widget.setStyleSheet("QPushButton#pushButton_login{\n"
"  background-color:qlineargradient(spread:pad,x1:0,y1:0.505682,x2:1,y2:0.477,stop:0 rgba(11,131,120,219),stop:1 rgba(85,98,112,226));\n"
"  color:rgba(255,255,255,210);\n"
"  border-radius:5px;\n"
"} \n"
"QPushButton#pushButton_login:hover{\n"
"  background-color:qlineargradient(spread:pad,x1:0,y1:0.505682,x2:1,y2:0.477,stop:0 rgba(150,123,111,219),stop:1 rgba(85,81,84,226));\n"
"  color:rgba(255,255,255,210);\n"
"  border-radius:5px;\n"
"} \n"
"QPushButton#pushButton_login:pressed{\n"
"  padding-left:5px;\n"
"  padding-top:5px;\n"
"  background-color:rgba(150,123,111,125);\n"
"}\n"
"QPushButton#pushButton_2{\n"
"  background-color:rgba(0,0,0,0);\n"
"  color:rgba(85,98,112,255);\n"
"} \n"
"QPushButton#pushButton_2:hover{\n"
"  color:rgba(131,96,53,255);\n"
"} \n"
"QPushButton#pushButton_2:pressed{\n"
"  padding-left:5px;\n"
"  padding-top:5px;\n"
"  color:rgba(91,88,53,255);\n"
"}\n"
"")
        self.widget.setObjectName("widget")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(360, 70, 321, 461))
        self.label_2.setStyleSheet("background-color:rgba(255,255,255,255);\n"
"border-bottom-right-radius:50px;\n"
"border-top-left-radius:50px;")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(440, 130, 171, 61))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color:rgba(0,0,0,200)")
        self.label_3.setObjectName("label_3")
        self.lineEdit_username = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_username.setGeometry(QtCore.QRect(420, 220, 201, 41))
        self.lineEdit_username.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color:rgba(0,0,0,240);\n"
"padding-bottom:7px;")
        self.lineEdit_username.setObjectName("lineEdit_username")
        self.lineEdit_password = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_password.setGeometry(QtCore.QRect(420, 290, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lineEdit_password.setFont(font)
        self.lineEdit_password.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color:rgba(0,0,0,240);\n"
"padding-bottom:7px;")
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.pushButton_login = QtWidgets.QPushButton(self.widget)
        self.pushButton_login.setGeometry(QtCore.QRect(410, 380, 221, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_login.setFont(font)
        self.pushButton_login.setStyleSheet("QPushButton#pushButton{\n"
"  background-color:qlineargradient(spread:pad, x1:0,y1:0.505682,x2:1,y2:0.477,stop:0 rgba(11,131,120,219),stop:1 rgba(85,98,112,226));\n"
"  color:rgba(255,255,255,210);\n"
"  border-radius:5px;\n"
"}\n"
"QPushButton#pushButton:hover{\n"
"  background-color:qlineargradient(spread:pad, x1:0,y1:0.505682,x2:1,y2:0.477,stop:0 rgba(150,123,111,219),stop:1 rgba(85,81,84,226));\n"
"}\n"
"QPushButton#pushButton:pressed{\n"
"  padding-left:5px;\n"
"  padding-top:5px;\n"
"  background-color:rgba(150,123,111,255)\n"
"}\n"
"\n"
"\n"
"")
        self.pushButton_login.setObjectName("pushButton_login")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setGeometry(QtCore.QRect(370, 460, 311, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:rgba(0,0,0,210);")
        self.label_4.setObjectName("label_4")
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setGeometry(QtCore.QRect(620, 80, 51, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("image: url(:/1/关闭.png);\n"
"")
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_3.setText(_translate("Form", "Log In"))
        self.lineEdit_username.setPlaceholderText(_translate("Form", "User Name"))
        self.lineEdit_password.setPlaceholderText(_translate("Form", "Password"))
        self.pushButton_login.setText(_translate("Form", "Log In"))
        self.label_4.setText(_translate("Form", "Friction corrosion tester"))
import text_rc
