from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import *
from anytree import Node, RenderTree
from User import *
import sys
import ctypes
import time

class MainUI(QMainWindow):
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
        self.form_name = "mainForm(" + str(screensize) + ")" + ".ui"
        form = None

        try:
            loader = QUiLoader()
            form = loader.load(self.form_name, None)
            self.setCentralWidget(form)
        except:
            loader = QUiLoader()
            form = loader.load("mainForm(1080).ui", None)
            self.setCentralWidget(form)

        self.setCentralWidget(form)

        #set Permission access
        self.profile = form.findChild(QLabel, "profile")
        self.menu = form.findChild(QComboBox, "comboBox")
        self.menu.activated[str].connect(self.changePage)

        #init Subwidget
        self.subWidget = form.findChild(QStackedWidget, "stackedWidget")
        self.subWidget.setCurrentIndex(0)

        #Edit Profile section components
        self.save_warn_label = form.findChild(QLabel, "save_warn_label")

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
        self.change_password_button = form.findChild(QPushButton, "change_password_button")

        self.save_button.clicked.connect(self.saveProfile)
        self.cancel_button.clicked.connect(self.backToMainPage)
        self.change_password_button.clicked.connect(self.changePassWordWidget)

        #Change password section component
        self.cur_password = form.findChild(QLineEdit, "cur_password")
        self.new_password = form.findChild(QLineEdit, "new_password")
        self.re_password = form.findChild(QLineEdit, "re_password")
        self.warn_change_label = form.findChild(QLabel, "warn_change_label")

        self.confirm_password_button = form.findChild(QPushButton, "confirm_password_button")
        self.cancel_password_button =  form.findChild(QPushButton, "cancel_password_button")

        self.confirm_password_button.clicked.connect(self.confirm_password)
        self.cancel_password_button.clicked.connect(self.backToProfilePage)

        #Permission Table component
        self.permission_tabel = form.findChild(QTableWidget, "Permission_table")
        self.permission_tabel.setColumnCount(7)
        self.permission_tabel.setRowCount(0)
        self.permission_tabel.resizeColumnsToContents()
        self.permission_tabel.resizeRowsToContents()
        self.permission_list = []

        #chatSystem
        self.chat_button = form.findChild(QPushButton, "chat_button")
        self.list_user = form.findChild(QListWidget, "list_user")
        self.isChatOpen = False
        self.list_user.move(-999, -999)
        self.online_user = []
        self.offline_user = []
        self.user_index = []
        self.chat_button.clicked.connect(self.chatOpenClose)
        self.list_user.itemDoubleClicked.connect(self.selectProfile)

    def saveProfile(self):
        self.parent.user.name = (self.name_line.text())
        self.parent.user.middle_name = (self.middlename_line.text())
        self.parent.user.last_name = (self.surname_line.text())
        self.parent.user.nickname = (self.nickname_line.text())
        self.parent.user.phone_number = self.phone_line.text()
        self.parent.user.email = self.email_line.text()
        #have more
        #send user(modified) back to server
        self.parent.send("updateProfile", self.parent.user)
        self.loadProfile()
        self.save_warn_label.setText("Profile already updated (saved)")

    def loadProfile(self):
        self.name_line.setText(self.parent.user.name)
        self.middlename_line.setText(self.parent.user.middle_name)
        self.surname_line.setText(self.parent.user.last_name)
        self.nickname_line.setText(self.parent.user.nickname)
        self.phone_line.setText(self.parent.user.phone_number)
        self.email_line.setText(self.parent.user.email)
        self.save_warn_label.setText("")

    def confirm_password(self):
        if self.cur_password.text() != self.parent.user.password:
            self.warn_change_label.setText("Wrong current password")
        elif self.re_password.text() == "" or self.new_password.text() == "":
            self.warn_change_label.setText("Please enter password")
        elif self.re_password.text() != self.new_password.text():
            self.warn_change_label.setText("Re-enter password wrong")
        elif not self.passwordValidation(self.new_password.text()):
            self.warn_change_label.setText("Password must contain digit and Capital letter")
        else:
            self.parent.user.password = self.new_password.text()
            self.parent.send("updateProfile", self.parent.user)
            self.warn_change_label.setText("Password Changed (Completed)")

    def changePassWordWidget(self):
        self.warn_change_label.setText("")
        self.new_password.setText("")
        self.cur_password.setText("")
        self.re_password.setText("")
        self.subWidget.setCurrentIndex(3)

    def backToMainPage(self):
        if self.menu.currentText() == "Edit Profile":
            self.subWidget.setCurrentIndex(0)

    def backToProfilePage(self):
        self.subWidget.setCurrentIndex(1)

    def chatOpenClose(self):
        if self.isChatOpen == False:
            self.isChatOpen = True
            if self.form_name == "mainForm(1440).ui":
                self.list_user.move(1690, 660)
                self.chat_button.move(1690,620)
            else:
                self.list_user.move(1450, 300)
                self.chat_button.move(1450,260)
            self.parent.send("getInitialInfo", None)
            if self.parent.departmentList is not None:
                for department in self.parent.departmentList:
                    for pre, fill, node in RenderTree(department.positionTree):
                        if node.name.employeeList is not None:
                            for userID in node.name.employeeList:
                                user = node.name.employeeList[userID]
                                #print(user.name + " " + user.last_name + " " + user.status)
                                if user.status == 'Online':
                                    self.online_user.append(user)
                                else:
                                    self.offline_user.append(user)
            else:
                self.list_user.clear()
                self.user_index.clear()
                self.offline_user.clear()
                self.online_user.clear()
                self.isChatOpen = False
                self.list_user.move(-999, -999)
                if self.form_name == "mainForm(1440).ui":
                    self.chat_button.move(1690, 1400)
                else:
                    self.chat_button.move(1450, 1040)
                self.chatOpenClose()

        else:
            self.list_user.clear()
            self.user_index.clear()
            self.offline_user.clear()
            self.online_user.clear()
            self.isChatOpen = False
            self.list_user.move(-999, -999)
            if self.form_name == "mainForm(1440).ui":
                self.chat_button.move(1690, 1400)
            else:
                self.chat_button.move(1450, 1040)
        self.user_index = self.online_user + self.offline_user
        for i in range(len(self.user_index)):
            user = self.user_index[i]
            self.list_user.addItem(QListWidgetItem(user.name + " " + user.last_name + "\t[" + user.status+"]"))
            if user.status == 'Online':
                row = self.list_user.item(i)
                row.setForeground(QBrush(Qt.green))
            else:
                row = self.list_user.item(i)
                row.setForeground(QBrush(Qt.red))

    def changePage(self):
        if self.menu.currentText() == "Main Page":
            self.subWidget.setCurrentIndex(0)
        elif self.menu.currentText() == "Edit Profile":
            print(self.parent.user)
            self.subWidget.setCurrentIndex(1)
            self.loadProfile()
        elif self.menu.currentText() == "Settings":
            self.subWidget.setCurrentIndex(2)
        elif self.menu.currentText() == "System":
            self.subWidget.setCurrentIndex(5)
            self.parent.send("getInitialInfo", None)
            if self.parent.departmentList is not None:
                row = 0
                for department in self.parent.departmentList:
                    for pre, fill, node in RenderTree(department.positionTree):
                        permission_list =  node.name.getPerMissionList()
                        for col in range(7):
                            if col == 0:
                                self.permission_tabel.setRowCount(row+1)
                                self.permission_tabel.setCellWidget(row, col, QLabel(node.name.name))
                            else:
                                self.box = QCheckBox()
                                if permission_list[col-1] == True:
                                    self.box.setCheckState(Qt.Checked)
                                self.permission_tabel.setCellWidget(row, col, self.box)
                                self.permission_list.append(self.box)
                        row += 1
            else:
                self.subWidget.setCurrentIndex(5)

    def selectProfile(self , item = None):
        user = self.user_index[self.list_user.currentRow()]
        self.parent.send("getUserInfo",user.username)
        self.parent.changePageMainSection("see_profile", None)

    def passwordValidation(self, password):
        isDigit = False
        isCapitalized = False
        for alp in password:
            if alp.isdigit():
                isDigit = True
            if alp.isupper():
                isCapitalized = True
        if not (isDigit and isCapitalized):
            return False
        return True

