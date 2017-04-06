from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import *
from User import *
import sys

class MainUI(QMainWindow):
    def __init__(self , parent = None):
        QMainWindow.__init__(self, None)
        #setting main window
        self.setMinimumSize(1280, 720)
        self.setWindowTitle("MBM v.0")
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("Images/background2.png")))
        self.setPalette(palette)
        self.parent = parent
        self.UIinit()

    # init UI form (attribute)
    def UIinit(self):
        #init mainWidget
        loader = QUiLoader()
        form = loader.load("mainForm.ui", None)
        self.setCentralWidget(form)
        self.profile = form.findChild(QLabel, "profile")
        self.menu = form.findChild(QComboBox, "comboBox")
        self.menu.activated[str].connect(self.changePage)

        #init Subwidget
        self.subWidget = form.findChild(QStackedWidget, "stackedWidget")
        self.subWidget.setCurrentIndex(0)

        #init components of sub Widget
        self.name_line = form.findChild(QLineEdit, "name_lineEdit")
        self.middlename_line = form.findChild(QLineEdit, "middlename_lineEdit")
        self.surname_line = form.findChild(QLineEdit, "surname_lineEdit")
        self.nickname_line = form.findChild(QLineEdit, "nickname_lineEdit")
        self.phone_line = form.findChild(QLineEdit, "phone_lineEdit")
        self.email_line = form.findChild(QLineEdit, "email_lineEdit")
        self.address_text = form.findChild(QTextEdit, "address_textEdit")
        self.bio_text = form.findChild(QTextEdit, "bio_textEdit")

        self.birth_edit = form.findChild(QDateEdit, "dateEdit")
        self.nation_box = form.findChild(QComboBox, "nation_box")
        self.position_box = form.findChild(QComboBox, "position_box")
        self.department_box = form.findChild(QComboBox, "department_box")
        self.save_button = form.findChild(QPushButton, "save_button")
        self.cancel_button = form.findChild(QPushButton, "cancel_button")
        self.save_button.clicked.connect(self.saveProfile)
        self.cancel_button.clicked.connect(self.loadProfile)

    def mainPageSlot(self):
        print("test")

    def settingSlot(self):
        print("test")

    def saveProfile(self):
        self.parent.user.name =  self.name_line.text()
        self.parent.user.middle_name = self.middlename_line.text()
        self.parent.user.last_name =  self.surname_line.text()
        #self.parent.user.nick_name = self.nickname_line.text()
        #self.parent.user.phone_number = self.phone_line.text()
        self.parent.user.email = self.email_line.text()
        self.loadProfile()
        print("save complete")
        print(self.parent.user)

    def loadProfile(self):
        self.name_line.setText(self.parent.user.name)
        self.middlename_line.setText(self.parent.user.middle_name)
        self.surname_line.setText(self.parent.user.last_name)
        #self.nickname_line.setText(self.parent.user.nick_name)
        #self.phone_line.setText(self.parent.user.phone_number)
        self.email_line.setText(self.parent.user.email)
        '''
        self.address_text
        self.bio_text
        
        self.birth_edit
        self.nation_box
        self.position_box
        self.department_box
        '''

    def changePage(self):
        if(self.menu.currentText() == "Main Page"):
            self.subWidget.setCurrentIndex(0)
        elif(self.menu.currentText() == "Edit Profile"):
            self.subWidget.setCurrentIndex(1)
            self.loadProfile()
        elif (self.menu.currentText() == "Settings"):
            self.subWidget.setCurrentIndex(2)

