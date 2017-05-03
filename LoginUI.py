from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import *
from User import *
import ctypes

class LoginUI(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, None)
        self.setMinimumSize(1280, 720)
        self.setWindowTitle("MBM v.0")
        self.parent = parent
        self.UIinit()

    #init UI form (attribute)
    def UIinit(self):
        #setForm Screen Size
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(1)
        form_name = "loginForm(" + str(screensize) + ")" + ".ui"
        form = None

        try:
            loader = QUiLoader()
            form = loader.load(form_name, None)
            self.setCentralWidget(form)
        except:
            loader = QUiLoader()
            form = loader.load("loginForm(1080).ui", None)
            self.setCentralWidget(form)

        self.user_id = form.findChild(QLineEdit, "lineEdit_1")
        self.password = form.findChild(QLineEdit, "lineEdit_2")

        self.login_button = form.findChild(QPushButton, "pushButton_1")
        self.signin_button = form.findChild(QPushButton, "pushButton_2")

        self.login_button.clicked.connect(self.logIn)
        self.signin_button.clicked.connect(self.signUp)

    #click button "log in"
    def logIn(self):
        user = User(self.user_id.text() , self.password.text())
        self.parent.changePageLoginSection("login", user)

    #click buttin "sign up"
    def signUp(self):
        self.parent.changePageLoginSection("register")
