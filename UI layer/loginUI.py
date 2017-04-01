from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import *
import sys


class LoginUI(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)
        self.setMinimumSize(1280, 720)
        self.setWindowTitle("MBM v.0")
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("Images/background.png")))
        self.setPalette(palette)
        self.UIinit()

    def UIinit(self):
        loader = QUiLoader()
        form = loader.load("loginForm.ui", None)
        self.setCentralWidget(form)

        self.edit1 = form.findChild(QLineEdit, "lineEdit_1")
        self.edit2 = form.findChild(QLineEdit, "lineEdit_2")

        self.button1 = form.findChild(QPushButton, "pushButton_1")
        self.button2 = form.findChild(QPushButton, "pushButton_2")

        icon = QIcon("Images/login.png")
        self.button1.setIcon(icon)
        self.button1.setIconSize(QSize(self.button1.size().width()-2,self.button1.size().height()-5 ))
        icon = QIcon("Images/signup.png")
        self.button2.setIcon(icon)
        self.button2.setIconSize(QSize(self.button1.size().width()-2,self.button1.size().height()-5 ))

        self.button1.clicked.connect(self.logIn)
        self.button2.clicked.connect(self.signUp)


    def logIn(self):
        print("login")

    def signUp(self):
        print("signup")


app = QApplication(sys.argv)
ui = LoginUI()
ui.show()
app.exec_()