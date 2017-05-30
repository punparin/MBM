from turtle import done

from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import *
from anytree import Node, RenderTree
from User import *
from Project import *
from Event import *
import sys
import ctypes
import time

class WorkUI(QMainWindow):
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
        self.form_name = "WorkForm(" + str(screensize) + ")" + ".ui"
        form = None

        try:
            loader = QUiLoader()
            form = loader.load(self.form_name, None)
            self.setCentralWidget(form)
        except:
            loader = QUiLoader()
            form = loader.load("WorkForm(1080).ui", None)
            self.setCentralWidget(form)

        self.setCentralWidget(form)

        #Work section components

        #work and status label
        self.work_title = form.findChild(QLabel, "work_title")
        self.status_label = form.findChild(QLabel, "status_label")

        #date
        self.create_date = form.findChild(QDateEdit, "create_date")
        self.due_date = form.findChild(QDateEdit, "due_date")

        #des
        self.description = form.findChild(QTextEdit, "description")

        #ListWidget
        self.task_widget = form.findChild(QListWidget, "task_widget")
        self.comment_widget = form.findChild(QListWidget, "comment_widget")
        self.user_widget = form.findChild(QListWidget, "user_widget")

        #line edit
        self.comment_edit = form.findChild(QLineEdit, "comment_edit")
        self.task_edit = form.findChild(QLineEdit, "task_edit")

        #user combo box
        self.user_box = form.findChild(QComboBox, "user_box")

        #all button
        self.edit_desciption = form.findChild(QPushButton, "edit_desciption")
        self.task_done = form.findChild(QPushButton, "task_done")
        self.add_task = form.findChild(QPushButton, "add_task")
        self.remove_task = form.findChild(QPushButton, "remove_task")
        self.send_comment = form.findChild(QPushButton, "send_comment")
        self.addUser = form.findChild(QPushButton, "addUser")
        self.removeUser = form.findChild(QPushButton, "removeUser")
        self.back_button = form.findChild(QPushButton, "back_button")

        #signal slot
        self.back_button.clicked.connect(self.back)
        self.edit_desciption.clicked.connect(self.editDesciption)
        self.add_task.clicked.connect(self.addTask)
        self.task_done.clicked.connect(self.setDone)
        self.remove_task.clicked.connect(self.removeTask)
        self.send_comment.clicked.connect(self.comment)
        self.addUser.clicked.connect(self.addMember)
        self.removeUser.clicked.connect(self.removeMember)

        #used attribute
        self.task_list = []
        self.all_user = []
        self.userInWork = []
        self.userInBox = []
        self.seeing = ""

    def addMember(self):
        if self.seeing == "Project":
            if self.user_box.currentIndex() == -1:
                return
            user = self.userInBox[self.user_box.currentIndex()]
            self.userInWork.append(user)
            self.parent.interest_work.memberList.append(user.username)
            self.user_widget.addItem(QListWidgetItem(user.name + " " + user.last_name + " [Project Member]"))
            self.parent.send('updateProject', self.parent.interest_work)
            self.userInBox.clear()
            self.user_box.clear()
            for user in self.all_user:
                isFound = False
                for userExist in self.userInWork:
                    if user.username == userExist.username:
                        isFound = True
                        break
                if isFound == False:
                    self.userInBox.append(user)
                    self.user_box.addItem(user.name + " " + user.last_name)
        else:
            if self.user_box.currentIndex() == -1:
                return
            user = self.userInBox[self.user_box.currentIndex()]
            self.userInWork.append(user)
            self.parent.interest_event.memberList.append(user.username)
            self.user_widget.addItem(QListWidgetItem(user.name + " " + user.last_name + " [Project Member]"))
            self.parent.send('updateProject', self.parent.interest_event)
            self.userInBox.clear()
            self.user_box.clear()
            for user in self.all_user:
                isFound = False
                for userExist in self.userInWork:
                    if user.username == userExist.username:
                        isFound = True
                        break
                if isFound == False:
                    self.userInBox.append(user)
                    self.user_box.addItem(user.name + " " + user.last_name)

    def removeMember(self):
        if self.seeing == "Project":
            if self.userInWork[self.user_widget.currentRow()].username == self.parent.interest_work.leader:
                return
            if self.user_widget.currentRow() == 0 or self.user_widget.currentRow() == -1:
                return
            self.userInWork.remove(self.userInWork[self.user_widget.currentRow()])
            cur = self.user_widget.currentItem()
            self.user_widget.removeItemWidget(cur)
            self.parent.interest_work.memberList.clear()
            for user in self.userInWork:
                self.parent.interest_work.memberList.append(user.username)
            self.user_widget.clear()
            self.userInBox.clear()
            self.user_box.clear()
            for user in self.userInWork:
                if user.username == self.parent.interest_work.leader:
                    self.user_widget.addItem(QListWidgetItem(user.name + " " + user.last_name + " [Project Leader]"))
                else:
                    self.user_widget.addItem(QListWidgetItem(user.name + " " + user.last_name + " [Project Member]"))
            for user in self.all_user:
                isFound = False
                for userExist in self.userInWork:
                    if user.username == userExist.username:
                        isFound = True
                        break
                if isFound == False:
                    self.userInBox.append(user)
                    self.user_box.addItem(user.name + " " + user.last_name)
            self.parent.send('updateProject', self.parent.interest_work)
        else:
            if self.userInWork[self.user_widget.currentRow()].username == self.parent.interest_event.leader:
                return
            if self.user_widget.currentRow() == 0 or self.user_widget.currentRow() == -1:
                return
            self.userInWork.remove(self.userInWork[self.user_widget.currentRow()])
            cur = self.user_widget.currentItem()
            self.user_widget.removeItemWidget(cur)
            self.parent.interest_event.memberList.clear()
            for user in self.userInWork:
                self.parent.interest_event.memberList.append(user.username)
            self.user_widget.clear()
            self.userInBox.clear()
            self.user_box.clear()
            for user in self.userInWork:
                if user.username == self.parent.interest_event.leader:
                    self.user_widget.addItem(QListWidgetItem(user.name + " " + user.last_name + " [Project Header]"))
                else:
                    self.user_widget.addItem(QListWidgetItem(user.name + " " + user.last_name ))
            for user in self.all_user:
                isFound = False
                for userExist in self.userInWork:
                    if user.username == userExist.username:
                        isFound = True
                        break
                if isFound == False:
                    self.userInBox.append(user)
                    self.user_box.addItem(user.name + " " + user.last_name)
            self.parent.send('updateEvent', self.parent.interest_event)

    def comment(self):
        if self.seeing == "Project":
            date = QDate.currentDate().toString("[dd/MM/yyyy] ")
            self.parent.interest_work.textList.append(date + self.parent.user.name + " :  " + self.comment_edit.text())
            self.comment_widget.addItem(QListWidgetItem(date+ self.parent.user.name + " :  " + self.comment_edit.text()))
            self.parent.send('updateProject', self.parent.interest_work)
            self.comment_edit.clear()
        else:
            date = QDate.currentDate().toString("[dd/MM/yyyy] ")
            self.parent.interest_event.textList.append(date + self.parent.user.name + " :  " + self.comment_edit.text())
            self.comment_widget.addItem(
            QListWidgetItem(date + self.parent.user.name + " :  " + self.comment_edit.text()))
            self.parent.send('updateEvent', self.parent.interest_event)
            self.comment_edit.clear()

    def removeTask(self):
        if self.task_widget.currentRow() == -1:
            return
        self.task_list.remove(self.task_list[self.task_widget.currentRow()])
        cur = self.task_widget.currentItem()
        self.task_widget.removeItemWidget(cur)
        self.parent.interest_work.taskList.clear()
        self.parent.interest_work.taskList += self.task_list
        self.parent.send('updateProject', self.parent.interest_work)
        self.task_widget.clear()
        for i in range(len(self.task_list)):
            self.task_widget.addItem(QListWidgetItem(self.task_list[i][0]))
            if self.task_list[i][1] == "Done":
                row = self.task_widget.item(i)
                row.setForeground(QBrush(Qt.green))
            else:
                row = self.task_widget.item(i)
                row.setForeground(QBrush(Qt.black))

    def setDone(self):
        if self.task_widget.currentRow() == -1:
            return
        self.task_list[self.task_widget.currentRow()][1] = "Done"
        cur = self.task_widget.currentItem()
        cur.setForeground(QBrush(Qt.green))
        self.task_widget.setCurrentItem(cur)
        self.parent.interest_work.taskList.clear()
        self.parent.interest_work.taskList += self.task_list
        self.parent.send('updateProject', self.parent.interest_work)

    def editDesciption(self):
        if  self.seeing == "Project":
            self.parent.interest_work.description = self.description.toPlainText()
            self.parent.send('updateProject', self.parent.interest_work)
        else:
            self.parent.interest_event.description = self.description.toPlainText()
            self.parent.send('updateEvent', self.parent.interest_event)

    def addTask(self):
        if self.task_edit.text() == "":
            return
        task = QListWidgetItem(self.task_edit.text())
        task.setForeground(QBrush(Qt.black))
        self.task_widget.addItem(task)
        self.task_list.append([self.task_edit.text(), "Not Done"])
        self.parent.interest_work.taskList.append([self.task_edit.text(), "Not Done"])
        self.parent.send('updateProject', self.parent.interest_work)
        self.task_edit.clear()

    def loadWork(self, work):
        self.user_box.clear()
        self.task_widget.clear()
        self.comment_widget.clear()
        self.user_widget.clear()
        self.task_list.clear()
        self.all_user.clear()
        self.userInWork.clear()
        doneLt = []
        notDoneLt =[]
        userLt = []
        if type(work) == type(Project(None,None)):
            self.seeing = "Project"
            self.task_widget.move(1170, 250)
            self.task_edit.move(1170, 740)
            self.task_done.move(1500, 770)
            self.add_task.move(1610, 770)
            self.remove_task.move(1720, 770)

            self.user_widget.move(1330, 830)
            self.user_box.move(1330, 1320)
            self.addUser.move(1610, 1350)
            self.removeUser.move(1720, 1350)
            self.user_widget.resize(501, 491)
            #all text and title
            self.work_title.setText(work.title)
            self.create_date.setDate(QDate(int(work.createdDate[2]),int(work.createdDate[1]),int(work.createdDate[0])))
            self.due_date.setDate(QDate(int(work.dueDate[2]),int(work.dueDate[1]),int(work.dueDate[0])))
            self.description.setPlainText(work.description)
            self.status_label.setText(work.status)
            #status label
            if work.status == "In Process":
                self.status_label.setStyleSheet("font: 75 14pt \"MS UI Gothic\"; background-color : ; color : green;")
            else:
                self.status_label.setStyleSheet("font: 75 14pt \"MS UI Gothic\"; background-color : ; color : black;")
            #task widget
            for task in work.taskList:
                if task[1] == "Done":
                    doneLt.append(task)
                else:
                    notDoneLt.append(task)
            self.task_list = doneLt + notDoneLt
            for i in range(len(self.task_list)):
                self.task_widget.addItem(QListWidgetItem(self.task_list[i][0]))
                if self.task_list[i][1] == "Done":
                    row = self.task_widget.item(i)
                    row.setForeground(QBrush(Qt.green))
                else:
                    row = self.task_widget.item(i)
                    row.setForeground(QBrush(Qt.black))

            #commnet Widget
            for line in work.textList:
                self.comment_widget.addItem(QListWidgetItem(str(line)))

            #user_Widget:
            if self.parent.departmentList is not None:
                self.isRequesting = False
                for department in self.parent.departmentList:
                    for pre, fill, node in RenderTree(department.positionTree):
                        if node.name.employeeList is not None:
                            for userID in node.name.employeeList:
                                user = node.name.employeeList[userID]
                                self.all_user.append(user)
            for user in work.memberList:
                for all in self.all_user:
                    if user == all.username:
                        self.userInWork.append(all)
            for user in self.userInWork:
                if user.username == self.parent.interest_work.leader:
                    self.user_widget.addItem(QListWidgetItem(user.name + " " + user.last_name + " [Project Leader]"))
                else:
                    self.user_widget.addItem(QListWidgetItem(user.name + " " + user.last_name + " [Project Member]"))

            for user in self.all_user:
                isFound = False
                for userExist in self.userInWork:
                    if user.username == userExist.username:
                        isFound = True
                        break
                if isFound == False:
                    self.userInBox.append(user)
                    self.user_box.addItem(user.name + " " + user.last_name)
        else:
            ## FOR EVENT
            self.seeing = "Event"
            self.remove_task.move(-999,-999)
            self.task_widget.move(-999, -999)
            self.task_edit.move(-999, -999)
            self.task_done.move(-999, -999)
            self.add_task.move(-999, -999)

            self.user_widget.move(1330, 330)
            self.user_box.move(1330, 1090)
            self.addUser.move(1610, 1120)
            self.removeUser.move(1720, 1120)
            self.user_widget.resize(501, 790)

            # all text and title
            self.work_title.setText("EVENT : " + work.title)
            self.create_date.setDate(QDate(int(work.createdDate[2]), int(work.createdDate[1]), int(work.createdDate[0])))
            self.due_date.setDate(QDate(int(work.dueDate[2]), int(work.dueDate[1]), int(work.dueDate[0])))
            self.description.setPlainText(work.description)
            self.status_label.setText(work.status)
            # status label
            if work.status == "In Process":
                self.status_label.setStyleSheet("font: 75 14pt \"MS UI Gothic\"; background-color : ; color : green;")
            else:
                self.status_label.setStyleSheet("font: 75 14pt \"MS UI Gothic\"; background-color : ; color : black;")
            # commnet Widget
            for line in work.textList:
                self.comment_widget.addItem(QListWidgetItem(str(line)))

            # user_Widget:
            if self.parent.departmentList is not None:
                self.isRequesting = False
                for department in self.parent.departmentList:
                    for pre, fill, node in RenderTree(department.positionTree):
                        if node.name.employeeList is not None:
                            for userID in node.name.employeeList:
                                user = node.name.employeeList[userID]
                                self.all_user.append(user)
            for user in work.memberList:
                for all in self.all_user:
                    if user == all.username:
                        self.userInWork.append(all)
            for user in self.userInWork:
                if user.username == self.parent.interest_event.leader:
                    self.user_widget.addItem(QListWidgetItem(user.name + " " + user.last_name + " [Event Header]"))
                else:
                    self.user_widget.addItem(QListWidgetItem(user.name + " " + user.last_name))

            for user in self.all_user:
                isFound = False
                for userExist in self.userInWork:
                    if user.username == userExist.username:
                        isFound = True
                        break
                if isFound == False:
                    self.userInBox.append(user)
                    self.user_box.addItem(user.name + " " + user.last_name)

    def back(self):
        self.parent.changePageWorkSection("back")


