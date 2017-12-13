import sys, math,os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore


width = 1024
height =500

class DashBoard(QWidget):
    Carvalue = {'speed': True, 'power': True, 'dirlight_L': True, 'dirlight_R': True, 'urgent_light': True,
                'headlight': True, 'gear': True, 'speed_gear': True}
    def __init__(self):
        super(QWidget,self).__init__()
        self.set_ui()
        self.set_power()
        self.setQTimer()    #设置定时器实现闪烁功能
        # self.i =0
        self.shinestate = False


    '''
    UI初始化程序
    '''
    def set_ui(self):
        #获取当前路径的上一路径
        self.path =os.path.dirname(os.getcwd())#取当前目录上一级目录
        # print(self.path)
        #设置窗口大小
        self.resize(width,height)
        # 创建无边框程序
        self.setWindowFlags(Qt.FramelessWindowHint)
        #创建一个速度指针
        self.set_speedpointer()
        #创建一个紧急图标
        self.set_light()

    '''
    定时器设置
    '''
    def setQTimer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.iconshine) #改变闪烁状态
        self.timer.start(1000) #设置闪烁频率

        # self.update_timer = QTimer(self)
        # self.update_timer.timeout.connect(self.update)
        # self.update_timer.start(1500)
        self.shinestate = False


    '''
    利用QPalette设置窗口背景图片,图片不能随着窗口变化而变化
    '''
    def set_background_palette(self):
        self.palette1 = QPalette()
        self.palette1.setBrush(QPalette.Background, QBrush(QPixmap(self.path+'dashboard\image\仪表盘.png')))  # 设置背景图片
        self.setPalette(self.palette1)


    '''
    利用Painter设置桌面背景
    '''
    def set_background_painter(self):
        self.painter =QPainter()
        self.painter.begin(self)
        self.painter.setRenderHint(QPainter.Antialiasing)
        self.painter.setPen(Qt.NoPen)
        __path = self.path+'/dashboard/image/仪表盘.png'
        #1024,500为窗口大小
        self.painter.drawPixmap(0,0,width,height,QPixmap(__path))
        self.painter.end()



    '''
    设置指针图片
    '''
    def set_speedpointer(self):
        self.speedpointer = QPixmap()  #创建一个pixmap对象
        self.speedpointer.load((self.path+'/dashboard/image/Pointery.png'))
        #重新计算指针大小以匹配表盘大小,缩放比例为3.5倍
        self.speedpointer_w =self.speedpointer.width()/3.5
        self.speedpointer_h =self.speedpointer.height()/3.5

    '''
    设置指针旋转
    '''
    def draw_speedponiter(self,angle):
        angle =40+DashBoard.Carvalue['speed'] /255 +160
        # print(angle)
        if(angle>300):
            angle =60
        painter =QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  #绘制图像反锯齿
        painter.translate(width/2,height/2)   #将坐标重新放置在窗口中央
        painter.save()
        painter.rotate(angle)
        #计算大小以及坐标
        painter.drawPixmap(-self.speedpointer_w/2,-35,self.speedpointer_w,self.speedpointer_h,self.speedpointer)
        painter.restore()
    '''
    设置显示电量图标
    '''
    def set_power(self):
        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setGeometry(QtCore.QRect(180, 460, 100, 20))
        self.progressBar.setProperty("value", 99)
        self.progressBar.setFormat(' ')
        self.set_power_value()
    '''
    设置电量
    '''
    def set_power_value(self):
        #根据电量显示不同的图标颜色
        if DashBoard.Carvalue['power'] >60:
            self.setStyleSheet("QProgressBar::chunk {   background-color: #009100; width: 10px;  margin: 0.5px;}")
        elif DashBoard.Carvalue['power'] <20:
            self.setStyleSheet("QProgressBar::chunk {   background-color: #FF0000; width: 10px;  margin: 0.5px;}")
        else:
            self.setStyleSheet("QProgressBar::chunk {   background-color: #D28000; width: 10px;  margin: 0.5px;}")
        self.progressBar.setProperty("value",DashBoard.Carvalue['power'])

    '''
    设置各个指示灯指示图标
    '''
    def set_light(self):
        #危险报警闪光灯
        self.urgent_pointer = QPixmap()  #创建一个pixmap对象
        self.urgent_pointer.load((self.path+'/dashboard/image/urgent.ico'))
        #重新计算指针大小以匹配表盘大小,缩放比例为3.5倍
        self.urgent_pointer_w =self.urgent_pointer.width()
        self.urgent_pointer_h =self.urgent_pointer.height()

        #左转弯灯
        self.left_light  = QPixmap()  #创建一个pixmap对象
        self.left_light.load((self.path+'/dashboard/image/left.png'))
        self.left_light_w =self.left_light.width()
        self.left_light_h =self.left_light.height()

        #右转弯灯
        self.right_light  = QPixmap()  #创建一个pixmap对象
        self.right_light.load((self.path+'/dashboard/image/right.png'))
        self.right_light_w =self.left_light.width()
        self.right_light_h =self.left_light.height()

        #大灯图标
        self.head_light  = QPixmap()  #创建一个pixmap对象
        self.head_light.load((self.path+'/dashboard/image/headlight.ico'))
        self.head_light_w =self.left_light.width()
        self.head_light_h =self.left_light.height()


    '''
    修改闪烁状态
    '''
    def iconshine(self):
        self.shinestate = not self.shinestate    #翻转闪烁状态

    '''
    画图标
    '''
    def draw_light(self):
        cmd_list=[]
        painter =QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  #绘制图像反锯齿
        dir_light_L = lambda : painter.drawPixmap((width-800-self.left_light_w*2)/2,100,self.left_light_w,self.left_light_h,self.left_light )
        dir_light_R = lambda : painter.drawPixmap((width+800)/2, 100, self.left_light_w, self.left_light_h, self.right_light)
        urgent_light= lambda : painter.drawPixmap((width-self.urgent_pointer_w)/2,380,self.urgent_pointer_w,self.urgent_pointer_h,self.urgent_pointer)
        head_light  = lambda : painter.drawPixmap((width - self.head_light_w) / 2, 100, self.head_light_w, self.head_light_h, self.head_light)
        lightfun_dict={'dirlight_L':dir_light_L,
                    'dirlight_R':dir_light_R,
                    'urgent_light':urgent_light,
                    'headlight':head_light}
        if (self.shinestate):
            for i in DashBoard.Carvalue:  #遍历参数
                if DashBoard.Carvalue[i] == True :
                    try:
                        lightfun_dict[i]()
                        # cmd_list.append(lightfun_dict[i])  # 添加执行列表
                    except:
                        None



    '''
    绘制事件
    '''
    def paintEvent(self,event):
        print('执行')
        self.set_background_painter()
        self.draw_speedponiter(77)
        self.draw_light()
        # self.set_power_value()
        # self.set_background()



