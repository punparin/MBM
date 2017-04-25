from PySide.QtGui import *
from PySide.QtUiTools import *
from User import *
import ctypes

class RegisterUI(QMainWindow):
    def __init__(self , parent = None):
        QMainWindow.__init__(self, None)
        self.setMinimumSize(1280, 720)
        self.setWindowTitle("MBM v.0")
        self.parent = parent
        self.UIinit()

    # init UI form (attribute)
    def UIinit(self):
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(1)
        form_name = "registerForm(" + str(screensize) + ")" + ".ui"
        form = None

        try:
            loader = QUiLoader()
            form = loader.load(form_name, None)
            self.setCentralWidget(form)
        except:
            loader = QUiLoader()
            form = loader.load("registerForm(1080).ui", None)
            self.setCentralWidget(form)
        self.setCentralWidget(form)

        self.user_id = form.findChild(QLineEdit, "lineEdit_1")
        self.password = form.findChild(QLineEdit, "lineEdit_2")
        self.email = form.findChild(QLineEdit, "lineEdit_3")
        self.comform_button = form.findChild(QPushButton, "pushButton")
        self.back_button = form.findChild(QPushButton, "pushButton_2")

        self.comform_button.clicked.connect(self.confirm)
        self.back_button.clicked.connect(self.back)
    # click button "confirm"
    def confirm(self):
        user = User(self.user_id.text(), self.password.text() , self.email.text())
        self.parent.changePageRegisterSection("register_confirm", user)

    def back(self):
        self.parent.changePageRegisterSection("back")


