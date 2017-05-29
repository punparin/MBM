from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import *
from anytree import Node, RenderTree
from Chat import*
from Project import*
from Event import*
import ctypes

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
        self.status_box = form.findChild(QComboBox, "status_box")
        self.isChatOpen = False
        self.isChatting = False
        self.isRequesting = False
        self.list_user.move(-999, -999)
        self.online_user = []
        self.offline_user = []
        self.user_index = []
        self.allDepartment = []
        self.allPosition = []

        self.chat_button.clicked.connect(self.chatOpenClose)
        self.status_box.activated[str].connect(self.changeStatus)
        self.list_user.itemDoubleClicked.connect(self.selectProfile)
        self.list_user.itemClicked.connect(self.openChat)

        #chatBox
        self.chat_box = form.findChild(QListWidget, "chat_box")
        self.chat_title = form.findChild(QPushButton, "chat_title")
        self.message = form.findChild(QLineEdit, "message")
        self.send_button = form.findChild(QPushButton, "send_button")
        self.exit_button = form.findChild(QPushButton, "exit_button")
        self.chat_box.move(-999, -999)
        self.chat_title.move(-999, -999)
        self.message.move(-999, -999)
        self.send_button.move(-999, -999)
        self.exit_button.move(-999, -999)
        self.exit_button.clicked.connect(self.exitChat)
        self.send_button.clicked.connect(self.sendMessage)
        self.messageList = []

        #Project and Event Section
        self.leader_list = []
        self.tab_widget = form.findChild(QTabWidget, "eventList")
        self.tab_widget.currentChanged.connect(self.eventChange)
        self.new_button = form.findChild(QPushButton, "new_button")
        self.new_button.clicked.connect(self.createWork)
        self.new_button.move(-999,-999)

        self.task_label = form.findChild(QLabel, "task_label")
        self.work_label = form.findChild(QLabel, "work_label")
        self.duedate_label = form.findChild(QLabel, "duedate_label")
        self.leader_label = form.findChild(QLabel, "leader_label")
        self.work_edit = form.findChild(QLineEdit, "work_edit")
        self.duedate_edit = form.findChild(QDateEdit, "duedate_edit")
        self.leader_box = form.findChild(QComboBox, "leader_box")

        self.confirm_work = form.findChild(QPushButton, "confirm_word")
        self.cancel_work = form.findChild(QPushButton, "cancel_work")
        self.cancel_work.clicked.connect(self.backToMainPage)
        self.confirm_work.clicked.connect(self.createConfirm)

    def createConfirm(self):
        title = self.work_edit.text()
        date = self.duedate_edit.date().toString("dd.MM.yyyy")
        leader = self.leader_box.currentText()

    def eventChange(self,index):
        self.new_button.move(1020, 800)
        if index == 1:
            self.new_button.setText("new project")
        elif index == 2:
            self.new_button.setText("new event")
        else:
            self.new_button.move(-999, -999)
            self.new_button.setText("")

    def createWork(self):
        self.subWidget.setCurrentIndex(4)
        for department in self.parent.departmentList:
            for pre, fill, node in RenderTree(department.positionTree):
                if node.name.employeeList is not None:
                    for userID in node.name.employeeList:
                        user = node.name.employeeList[userID]
                        self.leader_list.append(user)

        for user in self.leader_list:
            self.leader_box.addItem(user.name + " " + user.last_name)

        if self.new_button.text() == "new project":
            self.task_label.setText("Create Project")
            self.work_label.setText("Project Title :")
            self.duedate_label.setText("Due Date :")
            self.leader_label.setText("Project Leader :")
        else:
            self.task_label.setText("Create Event")
            self.work_label.setText("Event Title :")
            self.duedate_label.setText("Date :")
            self.leader_label.setText("Event Header :")

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
        self.subWidget.setCurrentIndex(0)
        if self.new_button.text() == "new project":
            self.tab_widget.setCurrentIndex(1)
        elif self.new_button.text() == "new event":
            self.tab_widget.setCurrentIndex(2)

    def backToProfilePage(self):
        self.subWidget.setCurrentIndex(1)

    def chatOpenClose(self):
        if self.isChatOpen == False:
            self.isChatOpen = True
            if self.form_name == "mainForm(1440).ui":
                self.list_user.move(1690, 660)
                self.chat_button.move(1690,620)
                self.status_box.move(2050, 630)
            else:
                self.list_user.move(1450, 300)
                self.chat_button.move(1450,260)
                self.status_box.move(1810, 270)
            if self.isRequesting == False:
                self.parent.send("getInitialInfo", None)
                self.isRequesting = True
            if self.parent.departmentList is not None:
                self.isRequesting = False
                for department in self.parent.departmentList:
                    for pre, fill, node in RenderTree(department.positionTree):
                        if node.name.employeeList is not None:
                            for userID in node.name.employeeList:
                                user = node.name.employeeList[userID]
                                if user.username == self.parent.user.username:
                                    continue
                                if user.status == 'Online':
                                    self.online_user.append(user)
                                else:
                                    self.offline_user.append(user)
                        self.allDepartment.append(department.name)
                        self.allPosition.append(node.name.name)
                        self.user_index.append(department.name)
                        self.user_index.append(node.name.name)
                        self.user_index += (self.online_user + self.offline_user)
            else:
                self.list_user.clear()
                self.user_index.clear()
                self.allPosition.clear()
                self.offline_user.clear()
                self.online_user.clear()
                self.isChatOpen = False
                self.list_user.move(-999, -999)
                self.status_box.move(-999, -999)
                if self.form_name == "mainForm(1440).ui":
                    self.chat_button.move(1690, 1400)
                    self.status_box.move(2050, 1410)
                else:
                    self.chat_button.move(1450, 1040)
                    self.status_box.move(1810, 1050)
        else:
            self.list_user.clear()
            self.user_index.clear()
            self.allPosition.clear()
            self.offline_user.clear()
            self.online_user.clear()
            self.isChatOpen = False
            self.list_user.move(-999, -999)
            if self.form_name == "mainForm(1440).ui":
                self.chat_button.move(1690, 1400)
                self.status_box.move(2050, 1410)
            else:
                self.chat_button.move(1450, 1040)
                self.status_box.move(1810, 1050)

        #add item to All User List Box
        for i in range(len(self.user_index)):
            user = self.user_index[i]
            if(user in self.allDepartment):
                self.list_user.addItem(QListWidgetItem(user))
                row = self.list_user.item(i)
                row.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            elif(user in self.allPosition):
                user = "      • " + user
                self.list_user.addItem(QListWidgetItem(user))
                row = self.list_user.item(i)
            else:
                self.list_user.addItem(QListWidgetItem("\t" + user.name + " " + user.last_name + "\t[" + user.status+"]"))
                if user.status == 'Online':
                    row = self.list_user.item(i)
                    row.setForeground(QBrush(Qt.green))
                elif user.status == 'Offline':
                    row = self.list_user.item(i)
                    row.setForeground(QBrush(Qt.red))
                elif user.status == 'Busy':
                    row = self.list_user.item(i)
                    row.setForeground(QBrush(Qt.red))
                elif user.status == 'Away':
                    row = self.list_user.item(i)
                    row.setForeground(QBrush(Qt.yellow))

    def updateAlluser(self, username, status):
        index = 0
        user = None
        for i in range(len(self.user_index)):
            if self.user_index[i] not in self.allPosition:
                if self.user_index[i].username == username:
                    index = i
                    user = self.user_index[i]
                    break
        if index == 0:
            return
        if status == 'Online':
            row = self.list_user.item(index)
            row.setText("\t" + user.name + " " + user.last_name + "\t[Online]")
            row.setForeground(QBrush(Qt.green))
        elif status == 'Offline':
            row = self.list_user.item(index)
            row.setText("\t" + user.name + " " + user.last_name + "\t[Offline]")
            row.setForeground(QBrush(Qt.red))
        elif status == 'Busy':
            row = self.list_user.item(index)
            row.setText("\t" + user.name + " " + user.last_name + "\t[Busy]")
            row.setForeground(QBrush(Qt.red))
        elif status == 'Away':
            row = self.list_user.item(index)
            row.setText("\t" + user.name + " " + user.last_name + "\t[Away]")
            row.setForeground(QBrush(Qt.yellow))

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
        if user in self.allDepartment or user in self.allPosition:
            return
        self.parent.send("getUserInfo",user.username)
        self.parent.changePageMainSection("see_profile", None)

    def changeStatus(self):
        self.parent.user.status = self.status_box.currentText()
        if self.status_box.currentText() == 'Online':
            self.status_box.setStyleSheet("background-color:rgb(171, 255, 156);")
        elif self.status_box.currentText() == 'Busy':
            self.status_box.setStyleSheet("background-color:rgb(255, 116, 116);")
        elif self.status_box.currentText() == 'Away':
            self.status_box.setStyleSheet("background-color:rgb(255, 250, 174);")
        self.parent.send("updateStatus", self.parent.user)

    def openChat(self, item = None):
        self.exitChat()
        self.isChatting = True
        user = self.user_index[self.list_user.currentRow()]
        if user in self.allDepartment or user in self.allPosition:
            return
        if self.form_name == "mainForm(1440).ui":
            self.chat_box.move(1220, 660)
            self.chat_title.move(1220, 620)
            self.message.move(1220, 1410)
            self.send_button.move(1590, 1410)
            self.exit_button.move(1620, 630)
        else:
            self.chat_box.move(980, 300)
            self.chat_title.move(980, 260)
            self.message.move(980, 1050)
            self.send_button.move(1350, 1050)
            self.exit_button.move(1390, 270)
        if self.isRequesting == False:
            self.parent.send("getUserInfo", user.username)
            self.isRequesting = True
        if self.parent.interest_user != None and self.parent.interest_user.username == user.username:
            self.isRequesting = False
            self.chat_title.setText(self.parent.interest_user.name + " " + self.parent.interest_user.last_name)
        else:
            self.openChat(None)
        try:
            path = "chatData\\" + self.parent.user.username + self.parent.interest_user.username + ".txt"
            file = open(path, "r")
            for line in file:
                self.chat_box.addItem(QListWidgetItem(line))
        except:
            path = "chatData\\" + self.parent.user.username + self.parent.interest_user.username + ".txt"
            file = open(path, "a")
            file.close()

    def updateChat(self):
        print("Chat Update")
        self.chat_box.clear()
        try:
            path = "chatData\\" + self.parent.user.username + self.parent.interest_user.username + ".txt"
            file = open(path, "r")
            for line in file:
                self.chat_box.addItem(QListWidgetItem(line))
        except:
            path = "chatData\\" + self.parent.user.username + self.parent.interest_user.username + ".txt"
            file = open(path, "a")
            file.close()

    def sendMessage(self):
        chat = Chat(self.parent.user.username, self.parent.interest_user.username)
        message = self.message.text()
        chat.message = message
        self.message.clear()
        self.parent.send("sendChat",chat)
        self.chat_box.addItem(QListWidgetItem("\n" + "You : " + message))
        if self.parent.interest_user.status == "Offline":
            self.chat_box.addItem(QListWidgetItem(self.parent.interest_user.name + "[offline] not recieve message"))
            index = self.chat_box.count()
            row = self.chat_box.item(index-1)
            row.setForeground(QBrush(Qt.red))
            return
        path = "chatData\\" + self.parent.user.username + self.parent.interest_user.username + ".txt"
        file = open(path, "a")
        file.write("\n" + "You : " +": " + message)
        file.close()

    def recieveMessage(self, chat):
        path = "chatData\\" + self.parent.user.username + chat.sender + ".txt"
        file = open(path, "a")
        file.write("\n" + chat.sender + " : " + chat.message)
        file.close()

    def exitChat(self):
        self.isChatting = False
        self.chat_box.move(-999, -999)
        self.chat_title.move(-999, -999)
        self.message.move(-999, -999)
        self.send_button.move(-999, -999)
        self.exit_button.move(-999, -999)
        self.chat_box.clear()
        self.message.clear()

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

