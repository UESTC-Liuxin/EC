from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Mainform import Ui_MainWindow
import setting_rc


class myMainform(Ui_MainWindow,QMainWindow):
    def __init__(self):
        super(myMainform,self).__init__()
        self.setupUi(self)













# if __name__ =="__main__":
#     app = QApplication(sys.argv)
#     form = myMainform()
#     form.show()
#     sys.exit(app.exec_())

