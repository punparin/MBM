import socket
from Handler import *
from UserManager import *
from ProjectManager import *
from DepartmentManager import *

class Server:
    def __init__(self, port=9999, maximumClient = 10):
        print("Initializing Server...")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.port = port
        self.maximumClient = maximumClient
        self.logFileName = 'serverLog'
        self.constant = 'constant'
        self.password = None
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(self.maximumClient)
            self.userManager = UserManager(self.socket)
            self.projectManager = ProjectManager(self.socket)
            self.departmentManager = DepartmentManager(self.userManager)
            print("The server is ready!")
            self.thread = threading.Thread(target=self.listen, args=[])
            self.thread.setDaemon(True)
            self.thread.start()

            self.command()
        except OSError:
            print("Server is already working!")

    # Get data from a secret file
    def getInformation(self):
        try:
            fileObject = open(self.constant, 'rb')
            self.password = pickle.load(fileObject)
            self.userManager.latestUserID = pickle.load(fileObject)
            fileObject.close()
        except FileNotFoundError:
            fileObject = open(self.constant, 'wb')
            self.password = 'admin'
            pickle.dump(self.password, fileObject)
            pickle.dump(0, fileObject)
            fileObject.close()
            print("The initial password is \'admin\', Please change the password as soon as possible")

    # Recieving command from user
    def command(self):
        print('Type \'cm\' to show all the command list ...')
        cm = input()
        while cm != 'exit':
            isCommandValid = False
            cms = cm.split()
            if cms[0] == 'cm':
                print('1) addAdmin [username] : to promote a user to be admin')
                print('2) delAdmin [username] : to demote an admin to be user')
                print('3) changePassword : to change the password')
                print('4) addDepartment [name] : to add a new department')
                isCommandValid = True
            # addAdmin
            elif cms[0] == 'addAdmin' and len(cms) == 2:
                pw = input("Password: ")
                if pw == self.password:
                    self.userManager.addAdmin(cms[1])
                else:
                    print('Invalid password')
                isCommandValid = True
            # delAdmin
            elif cms[0] == 'delAdmin' and len(cms) == 2:
                pw = input("Password: ")
                if pw == self.password:
                    self.userManager.delAdmin(cms[1])
                else:
                    print('Invalid password')
                isCommandValid = True
            # changePassword
            elif cms[0] == 'changePassword':
                self.changePassword()
                isCommandValid = True
            # addDepartment
            elif cms[0] == 'addDepartment' and len(cms) == 3:
                pw = input("Password: ")
                if pw == self.password:
                    self.departmentManager.addEmployee(cms[1], cms[2])
                else:
                    print('Invalid password')
                isCommandValid = True
            if not isCommandValid:
                print('Invalid Command')
            cm = input()

    def changePassword(self):
        currentPassword = input("Current Password: ")
        newPassword = input("New Password: ")
        confirmedNewPassword = input("Re-enter New Password: ")
        if currentPassword != self.password:
            print("Incorrect password")
        elif newPassword != confirmedNewPassword:
            print("Passwords are not the same")
        else:
            self.password = newPassword
            fileObject = open(self.passwordFileName, 'wb')
            pickle.dump(self.password, fileObject)
            fileObject.close()
            print("Changed password successfully")

    # Waiting for connection, then send the connection to Handler
    def listen(self):
        try:
            while True:
                clientSocket, address = self.socket.accept()
                print("Got a connection from %s" % str(address))
                thread = Handler(self.userManager, self.projectManager, clientSocket, address)
                thread.setDaemon(True)
                thread.start()
        except OSError:
            print("The port is not available")

def main():
    Server()

if __name__ == "__main__":
    main()
