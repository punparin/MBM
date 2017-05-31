from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import *
from anytree import Node, RenderTree
from User import *
import sys
import ctypes
import time

class ProfileUI(QMainWindow):
    def __init__(self , parent = None):
        QMainWindow.__init__(self, None)
        #setting main window
        self.setMinimumSize(1280, 720)
        self.setWindowTitle("MBM v.0")
        self.parent = parent
        self.UIinit()

    # init UI form (attribute)
    def UIinit(self):
        #init mainWidget
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(1)
        self.form_name = "ProfileForm(" + str(screensize) + ")" + ".ui"
        form = None

        try:
            loader = QUiLoader()
            form = loader.load(self.form_name, None)
            self.setCentralWidget(form)
        except:
            loader = QUiLoader()
            form = loader.load("ProfileForm(1080).ui", None)
            self.setCentralWidget(form)

        self.setCentralWidget(form)

        #Profile section components
        self.name_line = form.findChild(QLineEdit, "name_lineEdit")
        self.middlename_line = form.findChild(QLineEdit, "middlename_lineEdit")
        self.surname_line = form.findChild(QLineEdit, "surname_lineEdit")
        self.nickname_line = form.findChild(QLineEdit, "nickname_lineEdit")
        self.phone_line = form.findChild(QLineEdit, "phone_lineEdit")
        self.email_line = form.findChild(QLineEdit, "email_lineEdit")
        self.address_text = form.findChild(QTextEdit, "address_textEdit")
        self.bio_text = form.findChild(QTextEdit, "bio_textEdit")
        self.birth_edit = form.findChild(QLineEdit, "BirthDate")

        #other components
        self.project_list = form.findChild(QListWidget, "working")
        self.event_list = form.findChild(QListWidget, "joining")
        self.back_button = form.findChild(QPushButton, "back_button")

        self.back_button.clicked.connect(self.back)
    def loadProfile(self, user):
        self.name_line.setText(user.name)
        self.middlename_line.setText(user.middle_name)
        self.surname_line.setText(user.last_name)
        self.nickname_line.setText(user.nickname)
        self.phone_line.setText(user.phone_number)
        self.email_line.setText(user.email)
        self.self.address_text.setPlainText(user.address)
        self.bio_text.setPlainText(user.biology)
        self.birth_edit.setText(user.birth_date)

        for work in self.parent.projectList:
            if work.isMemberInProject(user.username):
                self.project_list.addItem(QListWidgetItem(work.title))

        for work in self.parent.eventList:
            if work.isMemberInEvent(user.username):
                self.event_list.addItem(QListWidgetItem(work.title))

    def back(self):
        self.parent.changePageProfileSection("back")


