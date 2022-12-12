
from statistics import mean
import sys
from traceback import print_tb
from PyQt5.QtWidgets import QWidget,QApplication
from PyQt5.QtCore import QThread, pyqtSignal,QObject
from time import sleep
import threading
from PyQt5.QtSerialPort import QSerialPort

class Serial_Qthread_function(QObject):
#建立一个信号
    signal_Srialstart_function   = pyqtSignal()
    signal_pushButton_Open       = pyqtSignal(object)#带参数的信号
    signal_pushButton_Open_flage = pyqtSignal(object)
    signal_ReadData              = pyqtSignal(object)
    signal_Send_data             = pyqtSignal(object)#信号连接到下面
    signal_Send_data_2           = pyqtSignal(object)
    signal_Send_data_3           = pyqtSignal(object)
   
    signal_Send_data_x0          = pyqtSignal(object)
    signal_Send_data_x1          = pyqtSignal(object)
    signal_pushButton_show2      = pyqtSignal(object)
    signal_pushButton_show2_stop       = pyqtSignal(object)
    signal_pushButton_show1_2    = pyqtSignal(object)
    signal_Send_data_y          = pyqtSignal(object)
    signal_Send_speed           = pyqtSignal(object)
    signal_Send_r               = pyqtSignal(object)
    signal_textEdit_receive_data =pyqtSignal(object)

    #signal_checkBox_HexView_time = pyqtSignal(object)

    def __init__(self,parent=None):
        super(Serial_Qthread_function,self).__init__(parent)
        print('初始化时候线程',threading.currentThread().ident)
        #开始调用网络的信号
        #定义串口状态
        self.state =0#0没有打开的状态,1串口已打卡，2串口已关闭


    #def slot_checkBox_HexView_time(self,state):
       # print("shijian",state)
    
    def slot_pushButton_Open(self,parameter):
        if self.state == 0:
           print(parameter)
           self.Serial.setPortName(parameter['comboBox_Com'])
           self.Serial.setBaudRate(int(parameter['comboBox_Baud']))

           if parameter['comboBox_Stop'] == '1.5':
               self.Serial.setStopBits(3)
           else:
               self.Serial.setStopBits(int(parameter['comboBox_Stop']))

           self.Serial.setDataBits(int(parameter['comboBox_Data']))
           
           setParity = 0
           if parameter['comboBox_Check'] == 'None':
               setParity = 0
           elif parameter['comboBox_Check'] == 'Odd':
               setParity = 3
           else:
               setParity = 2
            
           self.Serial.setParity(setParity)

           if self.Serial.open(QSerialPort.ReadWrite) == True:
               print('打开串口成功')
               self.state =1
               self.signal_pushButton_Open_flage.emit(self.state)

           else:
               print('打开失败')
               self.signal_pushButton_Open_flage.emit(0)

        else:
            print('关闭串口')
            self.state = 0
            self.Serial.close()
            self.signal_pushButton_Open_flage.emit(2)



    #接收函数
    def Serial_receive_data(self):
       
         self.signal_ReadData.emit(self.Serial.readAll())#接收


    def slot_Send_data(self,send_data):
        if self.state != 1 :#判断串口是否打开
            return
        if send_data['Hex'] ==2 :#如果是16进制的
            send_list  = []
            send_text = send_data['data']
            while send_text != '':
                try:
                    num = int(send_text[0:2],16)
                except:
                    #弹出一个提示框
                     #qw.QMessageBox.warning(self,'错误信息','请正确输入16进制数据')
                     return
                send_text =  send_text[2:].strip()#去空格
                send_list.append(num)
            input_s =bytes(send_list)
            self.Serial.write(input_s)#写入串口
        else:
            Byte_data = str.encode(send_data['data'])
            self.Serial.write(Byte_data)#写入串口

    def slot_Send_data_2(self,send_data_2):
            Byte_data = str.encode(send_data_2)
            self.Serial.write(Byte_data)#写入串口

    def slot_Send_data_3(self,send_data_3):
            Byte_data = str.encode(send_data_3)
            self.Serial.write(Byte_data)#写入串口

    def slot_Send_data_x0(self,send_data_x0):
            Byte_data = str.encode(send_data_x0)
            self.Serial.write(Byte_data)#写入串口
    def slot_Send_data_x1(self,send_data_x1):
            Byte_data = str.encode(send_data_x1)
            self.Serial.write(Byte_data)#写入串口
    def slot_Send_data_y(self,send_data_y):
            Byte_data = str.encode(send_data_y)
            self.Serial.write(Byte_data)#写入串口

    def slot_pushButton_show2(self,pushButton_show2):
            Byte_data = str.encode(pushButton_show2)
            self.Serial.write(Byte_data)#写入串口

    def slot_pushButton_show2_stop(self,pushButton_show2_stop):
            Byte_data = str.encode(pushButton_show2_stop)
            self.Serial.write(Byte_data)#写入串口

    
    def slot_pushButton_show1_2(self,pushButton_show1_2):
            Byte_data = str.encode(pushButton_show1_2)
            self.Serial.write(Byte_data)#写入串口

    def slot_pushButton_Send_speed(self,send_data1):
            Byte_data = str.encode(send_data1)
            self.Serial.write(Byte_data)#写入串口
    def slot_pushButton_Send_r(self,send_data2):
            Byte_data = str.encode(send_data2)
            self.Serial.write(Byte_data)#写入串口

    def SerialInit_function(self):
        sleep(1)
        print("串口线程id:",threading.current_thread().ident)
        self.Serial =QSerialPort()
        self.Serial.readyRead.connect(self.Serial_receive_data)#当它接收到数具后跳到接收函数



