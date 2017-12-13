# from smbus import SMBus
import dashboard
from uimng.back import *
import time



'''

   字节1表示车速 0~255代表   0~30KM/H
   字节2表示点亮 0~255代表   0~100%
           电量小于20%   红色显示
           电量20%~60%   黄色显示
           电量大于60%   绿色显示
   字节3
    D7 D6 D5 D4 D3 D2 D1 D0

 D0：0  N档
     1  D档
 D1：0  左方向灯关
     1  左方向灯开
 D2：0  右方向灯关
     1  右方向灯开
 D3：0  低速档
     1  高速档
 D5：0  大灯开
     1  大灯关
 D6：0  紧急灯关
     1  紧急灯开

'''



class GetI2cData():
       __iic_adress = 0x65
       def __init__(self):
              # self.bus = SMBus(1)
              self.__Carvalue = DashBoard.Carvalue.copy()
              #                  D7           D6                 D5          D4         D3               D2             D1           D0
              self.paralist = ['temp','urgent_light','headlight','temp','speed_gear','dirlight_R','dirlight_L','gear']

        
       def read_data(self):
              # self.__datalist= self.bus.read_i2c_block_data(self.__iic_adress,0,3)
              self.__datalist =[100,200,255]
              self.__Carvalue['speed'] = self.__datalist[0]/2 #获取第一个字节数据
              self.__Carvalue['power'] = self.__datalist[1]
              datatemp = self.__datalist[2]
              for i in range(len(self.paralist)):
                     if (datatemp >> (7-i))&0x01 ==1:
                            self.__Carvalue[self.paralist[i]] =  True
                     else :
                            self.__Carvalue[self.paralist[i]]  =False
       
       def check_change(self):
              for key in self.__Carvalue:
                     if self.__Carvalue[key] == DashBoard.Carvalue[key]:
                            continue
                     else:
                            DashBoard.Carvalue = self.__Carvalue.copy()
                            return 1
              return 0

               







        
