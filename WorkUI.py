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

        self.process_bar = form.findChild(QProgressBar, "process_bar")

        #date
        self.create_date = form.findChild(QDateEdit, "create_date")
        self.due_date = form.findChild(QDateEdit, "due_date")

        #des
        self.description = form.findChild(QLineEdit, "description")

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


    def loadWork(self, work):
        if type(work) == type(Project(None,None)):
            self.work_title.setText(work.title)
            self.create_date.setDate(QDate(int(work.createdDate[2]),int(work.createdDate[1]),int(work.createdDate[0])))
            self.due_date.setDate(QDate(int(work.dueDate[2]),int(work.dueDate[1]),int(work.dueDate[0])))

    def back(self):
        self.parent.changePageWorkSection("back")


