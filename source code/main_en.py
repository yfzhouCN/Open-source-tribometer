from statistics import mean
from tkinter import Y
from typing_extensions import Self
import PyQt5.QtCore
from importlib.resources import path
from ipaddress import AddressValueError
from multiprocessing.sharedctypes import Value
from socket import timeout
from turtle import pen
import time 

from PyQt5.QtCore import QThread ,QTimer,QBasicTimer
from PyQt5.QtWidgets import QWidget,QApplication,QMessageBox,QFileDialog,QProgressBar
from PyQt5.QtGui import QTextCursor,QColor,QIcon,QPixmap,QFont
import numpy as np
import sys,os
import PyQt5.QtWidgets as qw
import ui_serial
from serial_thread_1 import Serial_Qthread_function
from PyQt5.QtSerialPort import QSerialPortInfo
import ui_chart_en
import ui_chart2_en
import ui_chart3_en
import pyqtgraph as pg

class chartwidget(qw.QWidget):
    def __init__(self):
        super().__init__()
        self.ui2 = ui_chart_en.Ui_Form()
        self.ui2.setupUi(self)
        icon =QIcon()
        self.setWindowIcon(icon)
        self.setWindowTitle("Calibration steps")
    

class chart2widget(qw.QWidget):
    def __init__(self):
        super().__init__()
        self.ui3 = ui_chart2_en.Ui_Form()
        self.ui3.setupUi(self)
        icon =QIcon()
        self.setWindowIcon(icon)
        self.setWindowTitle("Motor driver wiring")

        self.ui3.pushButton.clicked.connect(self.close)#点击按钮后关闭

class chart3widget(qw.QWidget):
    def __init__(self):
        super().__init__()
        self.ui4 = ui_chart3_en.Ui_Form()
        self.ui4.setupUi(self)

        icon =QIcon()
        self.setWindowIcon(icon)

        self.setWindowTitle("Transmitter connection")

        self.ui4.pushButton.clicked.connect(self.close)#点击按钮后关闭



class SerialForm(qw.QWidget):
    def __init__(self):
        super().__init__()
        #初始化
        self.ui = ui_serial.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("Friction corrosion tester")
        
        self.Interface_Init()
        self.Ui_Init()

        icon =QIcon()
        self.setWindowIcon(icon)

        self.stateserial=0#定义了串口开没开的状态，防止忘了打开
        self.statetextreciral=0#定义了接受显示默认的状态，为o时显示在大的上面
        self.staterotate=0#定义了转速按钮的状态，当没有按下是0，按下后是1，清除接受又变成0
        self.statetime=0#定义了时间按钮的状态，当没有按下是0，按下后是1，清除接受又变成0
        self.stateload=0
        self.ckeckrotate=0#定义了勾选转速还是线速度的装填，当勾选转速时是0
        self.thresholdstate=0#定义了摩擦系数保护
        self.statethreshold=0#定义了有没有勾选保护
        self.pushButton_rotate=0#定义了转速按钮有没有按下，没按下是0
        self.state_pushButton_Send_speed=0#定义了线速度按钮有没有按下，没按下是0
        self.state_pushButton_radius=0#定义了半径按钮有没有按下，没按下是0

    #绘图
        self.pw = pg.PlotWidget()
        self.pw.setLabel('bottom','Time')
        self.pw.setLabel('left','Friction coefficient')
        self.pw.showGrid(x=True,y=True)#建立网格
        self.ui.verticalLayout.addWidget(self.pw)
        self.pl =self.pw.plot(pen ='g')#导入画笔绿色
             # 初始化全局变量
        self.list_data = []
        self.cnts = 0
 


#使线速度anniu失能
        self.ui.checkBox_speed_2.setChecked(True)
        self.ui.textEdit_Send_5.setDisabled(True)
#进度条
   #设置字体
        font = QFont()
        font.setBold(True)
        font.setWeight(30)
        self.ui.progressBar.setFont(font)
        # 设置一个值表示进度条的当前进度
        self.pv = 0
        # 申明一个时钟控件
        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.timerEvent)
        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.get_data_mean)
        self.timer3 = QTimer(self)
        self.timer3.timeout.connect(self.pushButton_threshold)



        # 设置进度条的范围
        self.ui.progressBar.setMinimum(0)
        self.ui.progressBar.setMaximum(100)
        self.ui.progressBar.setValue(self.pv)
        ## 设置进度条文字格式
        self.ui.progressBar.setFormat('Done  %p%'.format(self.ui.progressBar.value()-self.ui.progressBar.minimum()))



        self.w_chart = chartwidget()
        self.w_chart2 = chart2widget()
        self.w_chart3 = chart3widget()


#线程,连接信号,信号与槽
        self.port_name = []
        self.Serial_QTread = QThread()
        self.Serial_QTread_Function = Serial_Qthread_function()
        self.Serial_QTread_Function.moveToThread(self.Serial_QTread)
        self.Serial_QTread.start()
        self.Serial_QTread_Function.signal_Srialstart_function.connect( self.Serial_QTread_Function.SerialInit_function)
        self.Serial_QTread_Function.signal_Srialstart_function.emit()
        self.Serial_QTread_Function.signal_pushButton_Open.connect(self.Serial_QTread_Function.slot_pushButton_Open)
        self.Serial_QTread_Function.signal_pushButton_Open_flage.connect(self.slot_pushButton_Open_flage)
        self.Serial_QTread_Function.signal_ReadData.connect(self.slot_ReadData)
        self.Serial_QTread_Function.signal_Send_data.connect(self.Serial_QTread_Function.slot_Send_data)
        self.Serial_QTread_Function.signal_Send_data_2.connect(self.Serial_QTread_Function.slot_Send_data_2)
        self.Serial_QTread_Function.signal_Send_data_3.connect(self.Serial_QTread_Function.slot_Send_data_3)
        self.Serial_QTread_Function.signal_Send_data_x0.connect(self.Serial_QTread_Function.slot_Send_data_x0)
        self.Serial_QTread_Function.signal_Send_data_x1.connect(self.Serial_QTread_Function.slot_Send_data_x1)
        self.Serial_QTread_Function.signal_pushButton_show2.connect(self.Serial_QTread_Function.slot_pushButton_show2)
        self.Serial_QTread_Function.signal_pushButton_show2_stop.connect(self.Serial_QTread_Function.slot_pushButton_show2_stop)
        self.Serial_QTread_Function.signal_pushButton_show1_2.connect(self.Serial_QTread_Function.slot_pushButton_show1_2)
        self.Serial_QTread_Function.signal_Send_data_y.connect(self.Serial_QTread_Function.slot_Send_data_y)
        self.Serial_QTread_Function.signal_Send_r.connect(self.Serial_QTread_Function.slot_pushButton_Send_r)
        self.Serial_QTread_Function.signal_Send_speed.connect(self.Serial_QTread_Function.slot_pushButton_Send_speed)

        #定时搜索串口
        self.time_scan = QTimer()
        self.time_scan.timeout.connect(self.TimeOut_Scan)
        self.time_scan.start(1000)#用1秒钟去扫描

        self.ui.textEdit_receive_data.textChanged.connect(self.get_data)
       
    

    
    def get_data(self):#绘图
        self.txt = self.ui.textEdit_receive_data.toPlainText()
        data00 = self.txt.split('\n')
        
        if len(data00) <= 3 :
            data01 = None
        else:
            data01 = data00[3:-1]
        #data01= data00.pop()#列表去除最后一个数
        if data01 != [''] and data01 != None:
            data = [float(i) for i in data01]   
            data_=[]
            a1 = self.ui.textEdit_Send_4.toPlainText()
            a1 = float(a1)
            for i in data:
                i= i*5/(1023*a1)
                i=round(i,4)
                data_.append(i) 
            self.pl.setData(data_)

    def get_data_mean(self):#绘图
        self.txt = self.ui.textEdit_receive_data.toPlainText()
        data00 = self.txt.split('\n')
        
        if len(data00) <= 3 :
            data01 = None
        else:
            data01 = data00[3:-1]
        #data01= data00.pop()#列表去除最后一个数
        if data01 != [''] and data01 != None:
            data = [float(i) for i in data01]   
            data_=[]
            a1 = self.ui.textEdit_Send_4.toPlainText()
            a1 = float(a1)
            for i in data:
                i= i*5/(1023*a1)
                i=round(i,5)
                data_.append(i) 
                QApplication.processEvents()#刷新界面
            list_max=max(data_)#最大值
            list_min=min(data_)#最小值
            list_mean=mean(data_)#平均数
            list_mean=round(list_mean,5)#保留小数点后四位有效
            QApplication.processEvents()
            #print("qqqqqqq")
            self.ui.textEdit_receive_data_max.setPlainText(str(list_max))#先转换成字符串，
            self.ui.textEdit_receive_data_min.setPlainText(str(list_min))
            self.ui.textEdit_receive_data_mean.setPlainText(str(list_mean))
            if self.statethreshold==1 :#检查16进制的框框有没有被勾选
                y=self.ui.textEdit_Send.toPlainText()
                y=float(y)
                if list_max>=y:
                    
                    self.thresholdstate=1
                    self.timer3.isActive()
                    self.timer3.start(30)
                else:
                    self.thresholdstate=0
            else:
                pass  
        else:
            pass

    #定义搜索串口超时函数
    def TimeOut_Scan(self):
        #print('定时时间到')
        availablePort = QSerialPortInfo.availablePorts()#搜索串口
        new_port = []
        for port in  availablePort:
            new_port.append(port.portName())
        #print(new_port)

        if len(self.port_name) != len(new_port):
            self.port_name = new_port
            #print(self.port_name)
            self.ui.comboBox_Com.clear()
            self.ui.comboBox_Com.addItems(self.port_name)



#ui初始化
    def Interface_Init(self):
        self.Baud =('9600','57600','115200')
        self.Stop =('1','1.5','2')
        self.Data =('8','7','6','5')
        self.Check =('None','Odd','Even')
        self.ui.comboBox_Baud.addItems(self.Baud)#把东西填写到按键下
        self.ui.comboBox_Stop.addItems(self.Stop)
        self.ui.comboBox_Data.addItems(self.Data)
        self.ui.comboBox_Check.addItems(self.Check)
        self.ui.checkBox_threshold.stateChanged.connect(self.checkBox_threshold)#当checkBox_HexSend的状态改变时连接到下面checkBox_HexSend这个函数
        self.ui.checkBox_speed.stateChanged.connect(self.checkBox_speed)#当checkBox_HexSend的状态改变时连接到下面checkBox_HexSend这个函数
        self.ui.checkBox_speed_2.stateChanged.connect(self.checkBox_speed_2)
        self.ui.pushButton_Send_speed.clicked.connect(self.pushButton_Send_speed)
        self.ui.pushButton_Send.clicked.connect(self.pushButton_Send)#当pushButton_Send这个按钮点击的时候，连接到下面的pushButton_Send函数
        self.ui.pushButton_Send_2.clicked.connect(self.pushButton_2)
        self.ui.pushButton_Send_3.clicked.connect(self.pushButton_Send_3)
        self.ui.pushButton_ReceiveClean.clicked.connect(self.pushButton_ReceiveClean)
        self.ui.pushButton_SendClean.clicked.connect(self.pushButton_SendClean)
        self.ui.pushButton_SendClean_2.clicked.connect(self.pushButton_SendClean_2)
        self.ui.pushButton_SendClean_3.clicked.connect(self.pushButton_SendClean_3)
        self.ui.pushButton_save.clicked.connect(self.pushButton_save)
        self.ui.pushButton_show2.clicked.connect(self.pushButton_show2)#点击显示窗口
        self.ui.pushButton_show2_stop.clicked.connect(self.pushButton_show2_stop)#点击显示窗口
        self.ui.pushButton_show1_2.clicked.connect(self.pushButton_show1_2)#点击显示窗口
        self.ui.pushButton_show_bujin.clicked.connect(self.pushButton_show_bujin)
        self.ui.pushButton_x_0.clicked.connect(self.pushButton_x_0)
        self.ui.pushButton_x1.clicked.connect(self.pushButton_x1)
        self.ui.pushButton_show_chart3.clicked.connect(self.pushButton_show_chart3)
        self.ui.pushButton_kaishi.clicked.connect(self.pushButton_kaishi)
        self.ui.pushButton_SendClean_radius.clicked.connect(self.pushButton_SendClean_radius)
        self.ui.pushButton_SendClean_speed.clicked.connect(self.pushButton_SendClean_speed)
        self.ui.pushButton_Send_r.clicked.connect(self.pushButton_Send_r)
        self.ui.pushButton_Send_load.clicked.connect(self.pushButton_Send_load)
        self.ui.pushButton_SendClean_load.clicked.connect(self.pushButton_SendClean_load)
        self.ui.pushButton_Send.clicked.connect(self.pushButton_threshold1)

    def Ui_Init(self):
        #点击clicked可以连接到def pushButton_Open(self):
        self.ui.pushButton_Open.clicked.connect(self.pushButton_Open)
        
    def pushButton_Open(self):
        #创建一个新的空字典
        self.set_parameter ={}
        self.set_parameter['comboBox_Com']=self.ui.comboBox_Com.currentText()#取com的值
        self.set_parameter['comboBox_Baud']=self.ui.comboBox_Baud.currentText()#comboBox_Baud
        self.set_parameter['comboBox_Stop']=self.ui.comboBox_Stop.currentText()#comboBox_Sto
        self.set_parameter['comboBox_Data']=self.ui.comboBox_Data.currentText()#.comboBox_Data
        self.set_parameter['comboBox_Check']=self.ui.comboBox_Check.currentText()
        self.Serial_QTread_Function.signal_pushButton_Open.emit(self.set_parameter)#发信号到slot_pushButton_Open







    def slot_pushButton_Open_flage(self,sate):
        print('串口打开状态',sate)
        self.stateserial = sate
        if sate == 0:
            #弹出一个提示框
            qw.QMessageBox.warning(self,'Error message','The serial port has been occupied, open failed')#一个弹窗警告
        elif sate == 1:
            #让按键变红
            self.ui.pushButton_Open.setStyleSheet('color:yellow')
            #改变按键文字
            self.ui.pushButton_Open.setText('Close the serial port')
            self.time_scan.stop()#搜索串口关闭
        else:
             #让按键变红
            self.ui.pushButton_Open.setStyleSheet('color:black')
            #改变按键文字
            self.ui.pushButton_Open.setText('Open the serial port')
            self.time_scan.start(1000)#继续搜索串口


    def slot_ReadData(self,data):
        #print(data)
        #怎么让接收到的程序显示在界面上
        
        Byte_data =bytes(data)
        if self.statetextreciral==0:
                self.ui.textEdit_receive.insertPlainText(
                    Byte_data.decode('utf-8','ignore').strip('\n'))#吧接受到的数据添加到界面上
                self.ui.textEdit_receive.moveCursor(QTextCursor.End)  # 把光标显示在最后
        else:
                self.ui.textEdit_receive_data.insertPlainText(
                    Byte_data.decode('utf-8','ignore').strip('\n'))#吧接受到的数据添加到界面上
                self.ui.textEdit_receive_data.moveCursor(QTextCursor.End)  # 把光标显示在最后
               
                self.txt = self.ui.textEdit_receive_data.toPlainText()
                self.Serial_QTread_Function.signal_textEdit_receive_data.emit(self.txt)

    def pushButton_threshold(self):
        if self.thresholdstate==1:
            self.timer3.stop()
            print("电机转动紧急停止")
            pushButton_show1_2 ="s"
            self.Serial_QTread_Function.signal_pushButton_show1_2.emit(pushButton_show1_2)
            if self.timer1.isActive():
               self.timer1.stop()
               self.pv = 0
               self.ui.progressBar.setValue(self.pv)



   

    def checkBox_threshold(self,state):
        if state == 2:#选中16进制，可以将发送文本框中的数字变成16进制
            self.statethreshold=1
            print( self.statethreshold)
        else:#如果取消勾选，可以将发送文本框中的数字变回10进制
            self.statethreshold=0

    def checkBox_speed(self,state):
        if state == 2:#勾选
            self.ui.pushButton_Send_2.setDisabled(True)
            self.ui.pushButton_SendClean_2.setDisabled(True)
            self.ui.textEdit_Send_2.setDisabled(True)

        
            self.ui.pushButton_Send_speed.setEnabled(True)
            self.ui.pushButton_SendClean_speed.setEnabled(True)
            self.ui.textEdit.setEnabled(True)
            
            self.ckeckrotate=1
            self.ui.checkBox_speed_2.setChecked(False)
        else:
            self.ui.checkBox_speed_2.setChecked(True)

    def checkBox_speed_2(self,state):
        if state == 2:#勾选
            self.ui.pushButton_Send_2.setEnabled(True)
            self.ui.pushButton_SendClean_2.setEnabled(True)
            self.ui.textEdit_Send_2.setEnabled(True)

            
            self.ui.pushButton_Send_speed.setDisabled(True)
            self.ui.pushButton_SendClean_speed.setDisabled(True)
            self.ui.textEdit.setDisabled(True)
            self.ui.checkBox_speed.setChecked(False)
            self.ckeckrotate=0
        else:
            self.ui.checkBox_speed.setChecked(True)
        
    def pushButton_Send_speed(self):
        self.state_pushButton_Send_speed=1
        send_data1 ="w"+ self.ui.textEdit.toPlainText()#拿到sudu的一个字符
        self.Serial_QTread_Function.signal_Send_speed.emit(send_data1)
       
          
    def pushButton_Send_r(self):
        a = self.ui.textEdit_2.toPlainText()
        self.state_pushButton_radius=1
        if self.ckeckrotate==0:#当转速被勾选
                c =self.ui.textEdit_Send_2.toPlainText()
                a=float(a)
                c=float(c)
                b=2*3.1415926*a*0.1*c/60
                b=round(b,2)
                self.ui.textEdit.clear()
                self.ui.textEdit.setPlainText(str(b))
        else:#当线速度被勾选
            if self.state_pushButton_Send_speed==1:
                self.ui.textEdit_Send_2.clear()
                d=self.ui.textEdit.toPlainText()
    
                d=float(d)
                a=float(a)
                b=d*60/(2*3.1415926*0.1*a)
                b=round(b,5)
                
                
                self.ui.textEdit_Send_2.setPlainText(str(b))

                send_data2 ="q"+ self.ui.textEdit_2.toPlainText()#拿到sudu的一个字符
                self.Serial_QTread_Function.signal_Send_r.emit(send_data2)
            else:
                qw.QMessageBox.warning(self,'Warning','Please set speed')



    def pushButton_SendClean_load(self):
        self.ui.textEdit_Send_4.clear()

    def pushButton_Send(self):#需要把发送信号发送到串口线程
        print('点击发送按钮')
        send_data = {}#创建一个字典
        send_data["data"] = self.ui.textEdit_Send.toPlainText()#拿到它的一个字符
        #send_data["Hex"] = self.ui.checkBox_HexSend.checkState()#16进制的状态
        self.Serial_QTread_Function.signal_Send_data.emit(send_data)

    def pushButton_2(self):
        print('点击发送按钮2')
        a=self.ui.textEdit_Send_2.toPlainText()#拿到它的一个字符
        #print(a)
        #print(type(a))
        if str.isdigit(a)  == True :
            #print("正常")
            self.staterotate=1
            send_data_2 = "d" + a
            #print(send_data_2)
            self.Serial_QTread_Function.signal_Send_data_2.emit(send_data_2)
            self.pushButton_rotate=1#定义按下了转速健
        else :
            print("有英文")
            qw.QMessageBox.warning(self,'Warning','Please enter the numbers correctly')

    def pushButton_Send_load(self):
        
        self.stateload=1
        a=self.ui.textEdit_Send_4.toPlainText()
        a= "Load"+ ' '+ a+ "N"+"\n"
        self.ui.textEdit_receive.insertPlainText(a)
    def pushButton_threshold1(self):
        y=self.ui.textEdit_Send.toPlainText()
        y="Firction coefficient threshold"+" "+y+"\n"
        self.ui.textEdit_receive.insertPlainText(y)

    def pushButton_Send_3(self):#时间程序
        print('点击发送按钮3')
        a=self.ui.textEdit_Send_3.toPlainText()
        if str.isdigit(a)  == True :
                if self.pushButton_rotate==1 or self.state_pushButton_radius==1:
                    self.statetime=1
                    send_data_3 = "t"+  self.ui.textEdit_Send_3.toPlainText()#拿到它的一个字符
                    b=self.ui.textEdit_Send_2.toPlainText()
                    a=float(a)
                    b=float(b)
                    a1=a/b
                    a1=round(a1,2)
                    self.ui.textEdit_Send_5.clear()
                    self.ui.textEdit_Send_5.insertPlainText(str(a1))
                    self.Serial_QTread_Function.signal_Send_data_3.emit(send_data_3)
                else:
                    qw.QMessageBox.warning(self,'Warning','Please set rotate or speed、radius')
            


            
        else :
            print("有英文")
            qw.QMessageBox.warning(self,'Warning','Please enter the numbers correctly')

    def pushButton_x_0(self):
        print("点击发送x0")
        send_data_x0 ="x0"
        self.Serial_QTread_Function.signal_Send_data_x0.emit(send_data_x0)

    def pushButton_x1(self):
        print("点击发送x1")
        send_data_x1 ="x1"
        self.Serial_QTread_Function.signal_Send_data_x1.emit(send_data_x1)

    def pushButton_kaishi(self):#总的开始按钮，连接着进度条
        if self.stateserial == 1:#当打开串口后
            #if str.isdigit(a)  == True :#当输入负载后
            if self.stateload == 1 :#当输入负载后
                if self.staterotate == 1:
                    if self.statetime ==1:

                        print("点击发送y")
                        self.statetextreciral=1
                        send_data_y ="y1"
                        self.Serial_QTread_Function.signal_Send_data_y.emit(send_data_y)
                        if self.timer1.isActive() or self.timer2.isActive():
                            self.timer1.stop()
                            self.timer2.stop()
                        else:
                            #b1 = self.ui.textEdit_Send_2.toPlainText()#测试速度
                            #b1=float(b1)
                            #b1=(12/b1)#细分/测试速度/1000变成毫秒
                            self.timer1.start(1000)#进度条计时器
                            self.timer2.start(30000)
                    else:
                        qw.QMessageBox.warning(self,'Warning','Please set time')

                else:
                    qw.QMessageBox.warning(self,'Warning','Please set speed')

            else:
                 qw.QMessageBox.warning(self,'Warning','Please enter the load')

        else:
             qw.QMessageBox.warning(self, 'Warning', 'The serial port is not open')
            
    def timerEvent(self):
        self.pv += 1
        self.ui.progressBar.setValue(self.pv)
        a1=self.ui.textEdit_Send_5.toPlainText()#测试时间
        a1 = float(a1)
        a1_1=a1*60
        self.ui.progressBar.setMinimum(0)
        self.ui.progressBar.setMaximum(a1_1)
        self.ui.progressBar.setValue(self.pv)
        ## 设置进度条文字格式
        self.ui.progressBar.setFormat('Done  %p%'.format(self.ui.progressBar.value()-self.ui.progressBar.minimum()))
      
        if self.pv >a1_1:
            self.timer1.stop()
            self.pv = 0
            qw.QMessageBox.warning(self,'Tips','Please pay attention to save the data after the experiment is completed.')#一个弹窗警告




    def pushButton_ReceiveClean(self):
        print("清楚接收")
        self.ui.textEdit_receive.clear()#清楚文本框中的数据
        self.ui.textEdit_receive_data.clear()#清楚文本框中的数据
        self.ui.textEdit_receive_data_xishu.clear()
        self.ui.textEdit_receive_data_max.clear()
        self.ui.textEdit_receive_data_min.clear()
        self.ui.textEdit_receive_data_mean.clear()
        self.statetextreciral=0
        self.staterotate=0
        self.statetime=0
        self.stateload=0
        self.thresholdstate=0#定义了摩擦系数保护
        self.pushButton_rotate=0
        self.pushButton_rotate=0#定义了转速按钮有没有按下，没按下是0
        self.state_pushButton_Send_speed=0#定义了线速度按钮有没有按下，没按下是0
        self.state_pushButton_radius=0#定义了半径按钮有没有按下，没按下是0


        if self.timer1.isActive() or self.timer2.isActive():
            self.timer1.stop()
            self.timer2.stop()
        self.pv = 0
        self.ui.progressBar.setValue(self.pv)
        


    def pushButton_SendClean(self):
        print("清楚发送接收")
        self.ui.textEdit_Send.clear()#清楚文本框中的数据
        self.ui.textEdit_Send.moveCursor(QTextCursor.End)#把光标显示在最后

    def pushButton_SendClean_2(self):
        self.ui.textEdit_Send_2.clear()#清楚文本框中的数据
        self.ui.textEdit_Send_2.moveCursor(QTextCursor.End)#把光标显示在最后
    
    def pushButton_SendClean_3(self):
        self.ui.textEdit_Send_3.clear()#清楚文本框中的数据
        self.ui.textEdit_Send_5.clear()
        self.ui.textEdit_Send_3.moveCursor(QTextCursor.End)#把光标显示在最后
    
    def pushButton_SendClean_radius(self):
        self.ui.textEdit_2.clear()#清楚文本框中的数据
        self.ui.textEdit_Send_3.moveCursor(QTextCursor.End)#把光标显示在最后

    def pushButton_SendClean_speed(self):
        self.ui.textEdit.clear()#清楚文本框中的数据
        self.state_pushButton_Send_speed=0
        self.ui.textEdit_Send_3.moveCursor(QTextCursor.End)#把光标显示在最后



    def pushButton_save(self):#保存
        item_5= "Time"+"        "+"COF"+"\n"
        self.ui.textEdit_receive.insertPlainText(item_5)
        self.txt = self.ui.textEdit_receive_data.toPlainText()
        data00 = self.txt.split('\n')
        if len(data00) <= 3 :
            data01 = None
        else:
            data01 = data00[3:-1]
        #data01= data00.pop()#列表去除最后一个数
        if data01 != [''] and data01 != None:
            data = [float(i) for i in data01]   
            a1 = self.ui.textEdit_Send_4.toPlainText()
            a1 = float(a1)
            start=1
            for i,item in enumerate(data,start) :
                item= item*5/(1023*a1)
                item=round(item,5)
                QApplication.processEvents()
                i=i*0.1
                i=round(i,2)
                #item_1=str(item)+'  '+str(i)+' '+'s'+'\n'
                item_1=str(i)+"      "+str(item)+'\n'
                QApplication.processEvents()
                self.ui.textEdit_receive_data_xishu.insertPlainText(item_1)
            QApplication.processEvents()




        try:
            fileName, filetype = QFileDialog.getSaveFileName(self, "文件保存", "./save.txt", #默认起始路径
                                    "*(*.txt)")#第二个返回值filetype为文件筛选器类型,其中扩展名过滤,用双分号间隔
            if fileName == "":
                print("\n取消选择")
                return
            
        
            strRecv = self.ui.textEdit_receive.toPlainText() + self.ui.textEdit_receive_data_xishu.toPlainText()#获取接收的内容
        
            with open(fileName,'w')as f:#使用with as 语句，可进行异常处理，并在结束或错误时自动释放资源
                f.write(strRecv)
        except Exception as ex:#异常处理
            print("Save File Error:%s"%ex);#打印错误信息#print函数的格式，采用%带参数的方式，而不是c语言的可变参数的方式.字符串里面使用%s占位，在字符串后使用%替换值来替换.
    
    def pushButton_show2(self):
        self.statetextreciral=0
        self.w_chart.show()#点击打开窗口
        print("点击发送z")
        pushButton_show2 ="z"
        self.Serial_QTread_Function.signal_pushButton_show2.emit(pushButton_show2)
    def pushButton_show2_stop(self):
        self.w_chart.close()
        print("点击发送a")
        pushButton_show2_stop ="a"
        self.Serial_QTread_Function.signal_pushButton_show2_stop.emit(pushButton_show2_stop)
    def pushButton_show1_2(self):
        print("电机转动停止")
        pushButton_show1_2 ="s"
        self.Serial_QTread_Function.signal_pushButton_show1_2.emit(pushButton_show1_2)
        
        if self.timer1.isActive():
            self.timer1.stop()
        self.pv = 0
        self.ui.progressBar.setValue(self.pv)



    def pushButton_show_bujin(self):
        self.w_chart2.show()#点击打开窗口

    def pushButton_show_chart3(self):
        self.w_chart3.show()#点击打开窗口
    

if __name__=="__main__":
    app = qw.QApplication(sys.argv)
    
    w_en = SerialForm()
    w_en.show()
    sys.exit(app.exec())

