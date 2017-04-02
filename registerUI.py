from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import *
from User import *
import sys

class RegisterUI(QMainWindow):
    def __init__(self , parent = None):
        QMainWindow.__init__(self, None)
        self.setMinimumSize(1280, 720)
        self.setWindowTitle("MBM v.0")
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("Images/background.png")))
        self.setPalette(palette)
        self.parent = parent
        self.UIinit()

    # init UI form (attribute)
    def UIinit(self):
        loader = QUiLoader()
        form = loader.load("registerForm.ui", None)
        self.setCentralWidget(form)

        self.user_id = form.findChild(QLineEdit, "lineEdit_1")
        self.password = form.findChild(QLineEdit, "lineEdit_2")
        self.email = form.findChild(QLineEdit, "lineEdit_3")
        self.comform_button = form.findChild(QPushButton, "pushButton")

        self.comform_button.clicked.connect(self.confirm)

    # click button "confirm"
    def confirm(self):
        user = User(self.user_id.text(), self.password.text() , self.email.text())
        self.parent.changePageRegisterSection("register_confirm", user)


