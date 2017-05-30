from LoginUI import *
from RegisterUI import *
from MainUI import *
from ProfileUI import *
from WorkUI import *
from PySide.QtCore import *
from PySide.QtGui import *
from anytree import Node, RenderTree
from User import *
from Chat import *
import socket
import pickle
import sys
import threading

# Main UI / Client
class UImanager(QMainWindow):
    def __init__(self, host, port=9999):
        #Main UI set up
        QMainWindow.__init__(self, None)
        self.setMinimumSize(1280, 720)
        self.setWindowTitle("MBM")
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("Images/background.png")))
        self.setPalette(palette)

        #self.setWindowState(Qt.WindowMaximized)
        self.showFullScreen()

        # Init main Widget
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        login_widget = LoginUI(self)
        self.central_widget.addWidget(login_widget)

        # Init state attributes
        self.state = "offline"

        #add widget
        self.login_widget = LoginUI(self)
        self.main_widget = MainUI(self)
        self.register_widget = RegisterUI(self)
        self.profile_widget = ProfileUI(self)
        self.work_widget = WorkUI(self)
        self.central_widget.addWidget(self.login_widget)
        self.central_widget.addWidget(self.main_widget)
        self.central_widget.addWidget(self.register_widget)
        self.central_widget.addWidget(self.profile_widget)
        self.central_widget.addWidget(self.work_widget)

        # Init socket part
        self.isServerOnline = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.connect()

        if self.isServerOnline:
            # Init user
            self.user = None
            self.userThread = threading.Thread(target=self.waitingForUser, args=[])
            self.userThread.setDaemon(True)
            self.userThread.start()

        self.thread = threading.Thread(target=self.listen, args=[])
        self.thread.setDaemon(True)

        # Client Attribute
        self.departmentList = None
        self.interest_user = None
        self.interest_work = None
        self.currentChat = None
        self.projectList = None

    # Change page signal (send from log in UI page)
    def changePageLoginSection(self, signal = None, user = None):
        if signal == "login":
            self.state = "waiting"
            self.send('logIn', user)
            # Waiting for user to login
            while self.state == "waiting":
                pass
            if self.state == "online":
                self.centralWidget().setCurrentWidget(self.main_widget)
                if(self.user.isAdmin == True):
                    self.main_widget.menu.addItems(["System"])
                palette = QPalette()
                palette.setBrush(QPalette.Background, QBrush(QPixmap("Images/background2.png")))
                self.setPalette(palette)

        elif signal == "register":
            self.centralWidget().setCurrentWidget(self.register_widget)

    # Change Page signal (send from register UI page)
    def changePageRegisterSection(self, signal = None, user = None):
        if signal == "register_confirm":
            self.send('register', user)
            self.centralWidget().setCurrentWidget(self.login_widget)
        elif signal == "back":
            self.centralWidget().setCurrentWidget(self.login_widget)

    # Change Page signal (send from Main UI page)
    def changePageMainSection(self, signal=None, user=None):
        if signal == "see_profile":
            self.centralWidget().setCurrentWidget(self.profile_widget)
            self.profile_widget.loadProfile(self.interest_user)
            palette = QPalette()
            palette.setBrush(QPalette.Background, QBrush(QPixmap("Images/profile_background.png")))
            self.setPalette(palette)
        if signal == "see_work":
            self.work_widget.loadWork(self.interest_work)
            self.centralWidget().setCurrentWidget(self.work_widget)
            palette = QPalette()
            palette.setBrush(QPalette.Background, QBrush(QPixmap("Images/work_widget.png")))
            self.setPalette(palette)

    # Change Page signal (send from Profile UI page)
    def changePageProfileSection(self, signal=None, user=None):
        if signal == "back":
            self.centralWidget().setCurrentWidget(self.main_widget)
            palette = QPalette()
            palette.setBrush(QPalette.Background, QBrush(QPixmap("Images/background2.png")))
            self.setPalette(palette)

    # Change Page signal (send from Work UI page)
    def changePageWorkSection(self, signal=None, user=None):
        if signal == "back":
            self.main_widget.updateWork()
            self.centralWidget().setCurrentWidget(self.main_widget)
            self.main_widget.backToMainPage()
            self.main_widget.tab_widget.setCurrentIndex(1)
            palette = QPalette()
            palette.setBrush(QPalette.Background, QBrush(QPixmap("Images/background2.png")))
            self.setPalette(palette)
            self.send("getInitialProject",None)


    # Recieve task and object before logged in
    def waitingForUser(self):
        print('Waiting for User')
        try:
            while True:
                task = self.socket.recv(6).decode('ascii')
                if task == '':
                    break
                try:
                    obj = pickle.loads(self.socket.recv(4096))
                    self.state = "waiting"
                    # check if the user logged in successfully
                    if task == 'logIn' and type(obj) == User:
                        self.user = obj
                        self.user.status = "Online"
                        print("Initialize user successfully")
                        self.state = "online"
                        self.send("updateStatus",self.user)
                        break
                    # check if the user registered successfully
                    elif task == 'register' and obj is True:
                        print("Registered successfully")
                    else:
                        print("Invalid Username or Password")
                        self.state = "offline"
                        print(obj)
                except EOFError as e:
                    print(e)
            # Start listening for the server
            self.thread.start()
            self.send('getInitialInfo')
        except ConnectionResetError:
            # Completely terminate connection when the client disconnects
            print("The server is currently offline.")

    # Recieve task and object after logged in
    def listen(self):
        try:
            while True:
                print('listening')
                task = self.socket.recv(32).decode('ascii')
                if task == '':
                    pass
                try:
                    obj = pickle.loads(self.socket.recv(4096))
                    if task == 'getInitialInfo':
                        self.departmentList = obj
                        self.send("getInitialProject", None)
                    elif task == 'getUserInfo':
                        self.interest_user = obj
                        # obj in this case is a User instance without password
                    elif task == 'updateStatus':
                        username, status = obj
                        if self.main_widget.isChatOpen == True and username != self.user.username:
                            self.main_widget.updateAlluser(username,status)
                        else:
                            self.send("getInitialInfo", None)
                    elif task == 'recieveChat':
                        # chat is Chat instance
                        self.currentChat = obj
                        if self.main_widget.isChatting == True and self.interest_user.username == self.currentChat.sender:
                            self.main_widget.recieveMessage(self.currentChat)
                            self.main_widget.updateChat()
                        else:
                            self.main_widget.recieveMessage(self.currentChat)
                    elif task == 'getInitialProject':
                        # projectList is a tuple {} which contains project.title as a key and project itself as a value
                        self.projectList = obj
                        self.main_widget.updateWork()
                        self.main_widget.calendarUpdate()
                    elif task == 'updateProject':
                        self.interest_work = obj
                    elif task == 'getInitialEvent':
                        eventList = obj
                    elif task == 'updateEvent':
                        event = obj
                except EOFError as e:
                    print(e)
        except ConnectionResetError:
            # Completely terminate connection when the client disconnects
            print("The server is currently offline.")

    # Connect to the server
    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            msg = self.socket.recv(1024)
            print(msg.decode('ascii'))
            self.isServerOnline = True
        except ConnectionRefusedError:
            print("The server is currently offline.")

    # Send task and object
    def send(self, task, obj = None):
        print(task, str(obj))
        self.socket.send(task.encode('ascii'))
        obj = pickle.dumps(obj)
        self.socket.send(obj)

    # Close the socket connection
    def close(self):
        self.socket.close()

def main():
    app = QApplication(sys.argv)
    ui = UImanager(socket.gethostname())
    ui.show()
    app.exec_()

if __name__ == "__main__":
    main()
