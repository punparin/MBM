from loginUI import *
from registerUI import *
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import *
from User import *
import socket
import pickle
import sys

# Main UI / Client
class UImanager(QMainWindow):
    def __init__(self, host, port=9999):
        #Main UI set up
        QMainWindow.__init__(self, None)
        self.setMinimumSize(1280, 720)
        self.setWindowTitle("MBM v.0")
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("Images/background.png")))
        self.setPalette(palette)

        # Init main Widget
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        login_widget = LoginUI(self)
        self.central_widget.addWidget(login_widget)

        # Init socket part
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.connect()

    # Change page signal (send from log in UI page)
    def changePageLoginSection(self, signal = None, user = None):
        if signal == "login":
            print(user)
            self.send('logIn', user)
        elif signal == "register":
            register_widget = RegisterUI(self)
            self.central_widget.addWidget(register_widget)
            self.centralWidget().setCurrentWidget(register_widget)

    # Change Page signal (send from register UI page)
    def changePageRegisterSection(self, signal = None, user = None):
        if signal == "register_confirm":
            print(user)
            self.send('register', user)
            login_widget = LoginUI(self)
            self.central_widget.addWidget(login_widget)
            self.centralWidget().setCurrentWidget(login_widget)

    def connect(self):
        self.socket.connect((self.host, self.port))
        msg = self.socket.recv(1024)
        print(msg.decode('ascii'))

    def send(self, task, obj):
        self.socket.send(task.encode('ascii'))
        obj = pickle.dumps(obj)
        self.socket.send(obj)

    def close(self):
        self.socket.close()

def main():
    app = QApplication(sys.argv)
    ui = UImanager(socket.gethostname())
    ui.show()
    app.exec_()

if __name__ == "__main__":
    main()