# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\chart3_english.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(822, 521)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 20, 801, 411))
        self.label.setStyleSheet("image: url(:/1/传感器接线图english.png);\n"
"")
        self.label.setText("")
        self.label.setObjectName("label")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(690, 430, 120, 80))
        self.widget.setStyleSheet("QPushButton#pushButton{\n"
"  background-color:rgba(0,0,0,0);\n"
"  color:rgba(85,98,112,255);\n"
"} \n"
"QPushButton#pushButton:hover{\n"
"  color:rgba(131,96,53,255);\n"
"} \n"
"QPushButton#pushButton:pressed{\n"
"  padding-left:5px;\n"
"  padding-top:5px;\n"
"  color:rgba(91,88,53,255);\n"
"}")
        self.widget.setObjectName("widget")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 101, 61))
        self.pushButton.setStyleSheet("image: url(:/1/关闭.png);")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
import text_rc
