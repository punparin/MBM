import socket
import time
from Handler import *
from UserManager import *
from ProjectManager import *
from EventManager import *
from DepartmentManager import *

class Server:
    def __init__(self, port=9999, maximumClient = 10):
        print("Initializing Server...")
        start = time.time()
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = port
        self.maximumClient = maximumClient
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logFileName = 'serverLog'
        self.constant = 'constant'
        self.password = None
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(self.maximumClient)
            self.userManager = UserManager()
            self.projectManager = ProjectManager(self.socket)
            #self.eventManager = EventManager(self.socket)
            self.departmentManager = DepartmentManager(self.userManager)
            print("\n--- Server is Online ---")
            print("IP:", self.host, "Port:", self.port)
            print("Initial Runtime:", format((time.time() - start) / 1000, '.10f'), "sec")
            self.thread = threading.Thread(target=self.listen, args=[])
            self.thread.setDaemon(True)
            self.thread.start()
            self.getInformation()
            self.command()
        except OSError as err:
            print(err)
            print("\n!!! Server is already working !!!")

    # Get data from a secret file
    def getInformation(self):
        try:
            fileObject = open(self.constant, 'rb')
            self.password = pickle.load(fileObject)
            fileObject.close()
            if self.password == 'admin':
                print("The initial password is \'admin\', Please change the password as soon as possible\n")
        except FileNotFoundError:
            fileObject = open(self.constant, 'wb')
            self.password = 'admin'
            pickle.dump(self.password, fileObject)
            fileObject.close()
            print("The initial password is \'admin\', Please change the password as soon as possible\n")

    # Recieving command from user
    def command(self):
        isSafeMode = False
        pwd = ""
        while pwd != self.password:
            pwd = input("Password: ")
        print('\nType \'cm\' to show all the command list ...')
        while True:
            isCommandValid = False
            cm = input("\n")
            cms = cm.split()
            if len(cms) == 0:
                pass
            elif cms[0] == 'cm':
                print('\nCatagory:')
                print('1) Server')
                print('2) User')
                print('3) Department')
                print("Press a number to show commands for a specific catagory or any key to exit")
                cat = input("\nCommand: ")
                if cat == '1':
                    print('Server:')
                    print('\t- stop : to terminate the server')
                    print("\t- changePassword : to change the server's password")
                    print('\t- safeMode: to lock all commands')
                    print('\t- addAdmin [username] : to promote a user to be admin')
                    print('\t- removeAdmin [username] : to demote an admin to be user')
                elif cat == '2':
                    print('User:')
                    print('\t- findUser [username] : to show information of a user by username')
                    print('\t- createUser [username] [password] [email] : to register a new user')
                    print('\t- removeUser [username] : to remove a user')
                    print('\t- removeUserList : tp remove all users')
                    print('\t- showUserList : to show all users information')
                elif cat == '3':
                    print('Department:')
                    print('\t- addDepartment [name] : to add a new department')
                    print('\t- removeDepartment [department] : to remove a department')
                    print('\t- showDepartment [department] : to show information of a department')
                    print('\t- showDepartmentList : to show information of all departments')
                    print('\t- addPosition [department] [position] [parentPosition] : to add a new position to a department (parentPosition can be empty)')
                    print('\t- removePosition [department] [position] : to remove a position from a department')
                    print('\t- addEmployee [department] [position] [username] : to add a new employee to a department')
                    print('\t- removeEmployee [department] [username] : to remove an employee from a department')
                    print('\t- findEmployeePosition [department] [username] : to find a current position of a user')
                isCommandValid = True
            # stop
            elif cms[0] == 'stop':
                break
            # safeMode
            elif cms[0] == 'safeMode':
                isSafeMode = True
                break
            # addAdmin
            elif cms[0] == 'addAdmin' and len(cms) == 2:
                print()
                self.userManager.addAdmin(cms[1])
                isCommandValid = True
            # delAdmin
            elif cms[0] == 'removeAdmin' and len(cms) == 2:
                print()
                self.userManager.delAdmin(cms[1])
                isCommandValid = True
            # changePassword
            elif cms[0] == 'changePassword':
                self.changePassword()
                isCommandValid = True
            # addDepartment
            elif cms[0] == 'addDepartment' and len(cms) == 2:
                print()
                self.departmentManager.addDepartment(cms[1])
                isCommandValid = True
            # addEmployee
            elif cms[0] == 'addEmployee' and len(cms) == 4:
                print()
                self.departmentManager.addEmployee(cms[1], cms[2], cms[3])
                isCommandValid = True
            # showDepartmentList
            elif cms[0] == 'showDepartmentList':
                self.departmentManager.showDepartmentList()
                isCommandValid = True
            # removeDepartment
            elif cms[0] == 'removeDepartment' and len(cms) == 2:
                print()
                self.departmentManager.removeDepartment(cms[1])
                isCommandValid = True
            # findUser
            elif cms[0] == 'findUser' and len(cms) == 2:
                print()
                self.userManager.findUserByUsername(cms[1])
                isCommandValid = True
            # createUser
            elif cms[0] == 'createUser' and len(cms) == 4:
                print()
                self.userManager.registerUser(User(cms[1], cms[2], cms[3]))
                isCommandValid = True
            # removeUser
            elif cms[0] == 'removeUser' and len(cms) == 2:
                print()
                self.userManager.removeUser(cms[1])
                isCommandValid = True
            # removeUserList
            elif cms[0] == 'removeUserList' and len(cms) == 1:
                print()
                self.userManager.removeUserList()
                isCommandValid = True
            # showUserList
            elif cms[0] == 'showUserList' and len(cms) == 1:
                print()
                self.userManager.showUserList()
                isCommandValid = True
            # addPosition
            elif cms[0] == 'addPosition':
                if len(cms) == 3:
                    print()
                    self.departmentManager.addPosition(cms[1], cms[2])
                    isCommandValid = True
                elif len(cms) == 4:
                    print()
                    self.departmentManager.addPosition(cms[1], cms[2], cms[3])
                    isCommandValid = True
            # removePosition
            elif cms[0] == 'removePosition' and len(cms) == 3:
                print()
                self.departmentManager.removePosition(cms[1], cms[2])
                isCommandValid = True
            # removeEmployee
            elif cms[0] == 'removeEmployee' and len(cms) == 3:
                print()
                self.departmentManager.removeEmployee(cms[1], cms[2])
                isCommandValid = True
            # showDepartment
            elif cms[0] == 'showDepartment' and len(cms) == 2:
                print()
                self.departmentManager.showDepartment(cms[1])
                isCommandValid = True
            # findEmployeePosition
            elif cms[0] == 'findEmployeePosition' and len(cms) == 3:
                print()
                self.departmentManager.findEmployeePosition(cms[1], cms[2])
                isCommandValid = True
            if not isCommandValid:
                print('Invalid Command')
        if isSafeMode:
            self.command()

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
            fileObject = open(self.constant, 'wb')
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
