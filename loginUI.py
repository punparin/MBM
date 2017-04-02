from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import *
from User import *

class LoginUI(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, None)
        self.setMinimumSize(1280, 720)
        self.setWindowTitle("MBM v.0")
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("Images/background.png")))
        self.setPalette(palette)
        self.parent = parent
        self.UIinit()

    #init UI form (attribute)
    def UIinit(self):
        loader = QUiLoader()
        form = loader.load("loginForm.ui", None)
        self.setCentralWidget(form)

        self.user_id = form.findChild(QLineEdit, "lineEdit_1")
        self.password = form.findChild(QLineEdit, "lineEdit_2")

        self.login_button = form.findChild(QPushButton, "pushButton_1")
        self.signin_button = form.findChild(QPushButton, "pushButton_2")

        icon = QIcon("Images/login.png")
        self.login_button.setIcon(icon)
        self.login_button.setIconSize(QSize(self.login_button.size().width()-2,self.login_button.size().height()-5 ))
        icon = QIcon("Images/signup.png")
        self.signin_button.setIcon(icon)
        self.signin_button.setIconSize(QSize(self.signin_button.size().width()-2,self.signin_button.size().height()-5 ))

        self.login_button.clicked.connect(self.logIn)
        self.signin_button.clicked.connect(self.signUp)

    #click button "log in"
    def logIn(self):
        user = User(self.user_id.text() , self.password.text())
        self.parent.changePageLoginSection("login", user)

    #click buttin "sign up"
    def signUp(self):
        self.parent.changePageLoginSection("register")
