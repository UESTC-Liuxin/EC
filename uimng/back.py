import sys,threading,time,os
sys.path.append("..")
from dashboard.dashboard import *
from uimng.myMainform import *
from uimng.read_data import *









class BackThread(QThread):#为了引入信号与槽，将QThread引入继承
    updat_signal =pyqtSignal()   #定义一个信号
    def __init__(self):
        super(BackThread, self).__init__()
        self.car=DashBoard() #开启仪表盘
        self.main=myMainform()  #开启桌面
        self.Slot_connect()
        self.main.show()
        self.read = GetI2cData()
        self.start()             #开启监控线程



    def Slot_connect(self):
        self.main.settingbtn.clicked.connect(self.Mainform_show)
        # self.main.musicbtn.clicked.connect()
        # self.main.radiobtn.clicked.connect()
        # pass

    def Mainform_show(self):
        print('触发信号')
        self.car.show()

        # self.main.close()




    def CarInstrument_show(self,cmd):
        if cmd ==True:
            self.car.show()
        else:
            pass



    def run(self):
        while True:
            time.sleep(1)
            #查询速度
            #查询汽车行驶状态
            #查询灯的状态
            #当有突发信号，立即更新UI
            self.read.read_data()
            self.read.check_change()
            self.car.update()
            # if self.read.check_change():
            #     self.car.update()
            #     print('已经改变')






if __name__ == '__main__':
    app = QApplication(sys.argv)
    back = BackThread()
    sys.exit(app.exec_())

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     car = DashBoard()
#     car.show()
#     print(os.getcwd())
#     sys.exit(app.exec_())
