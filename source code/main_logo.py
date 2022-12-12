import sys
from PyQt5.QtWidgets import QWidget,QApplication
from pip import main
import begin
import PyQt5.QtWidgets as qw
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import main_en


class InitForm(qw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = begin.Ui_Form()
        self.ui.setupUi(self)


        self.ui.pushButton_login.clicked.connect(self.pushButton_login)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2)

        
    
    def pushButton_login(self):
        #print(self.ui.lineEdit_username.text())
        #print(self.ui.lineEdit_password.text())
        if self.ui.lineEdit_username.text() == "123" and self.ui.lineEdit_password.text() == "123":
                print("english")
                begin_wi.close()
                main_ui_en.show()
        else:
             qw.QMessageBox.warning(self,'Warning','The password or account is incorrect')#一个弹窗警告

    def pushButton_2(self):
        begin_wi.close()




if __name__ == "__main__":

    app = QApplication(sys.argv)
    begin_wi = InitForm()
    main_ui_en = main_en.SerialForm()
    begin_wi.show()
    sys.exit(app.exec_())
