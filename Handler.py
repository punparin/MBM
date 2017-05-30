import threading
from UserManager import *

class Handler(threading.Thread):
    def __init__(self, userManager, projectManager, eventManager, chatManager, departmentManager, clientSocket, address):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
        self.userManager = userManager
        self.chatManager = chatManager
        self.departmentManager = departmentManager
        self.projectManager = projectManager
        self.eventManager = eventManager
        self.address = address
        self.currentUsername = None
        self.logFileName = 'companyLog'
        self.companyName = None
        self.userManagerTasks = ['logIn', 'register', 'updateProfile', 'getUserInfo', 'updateStatus']
        self.projectManagerTasks = ['createProject', 'searchProject', 'updateProject', 'removeProject', 'getInitialProject']
        self.eventManagerTasks = ['createEvent', 'searchEvent', 'updateEvent', 'removeEvent', 'getInitialEvent']
        self.departmentManagerTasks = ['addDepartment', 'removeDepartment', 'getInitialInfo', 'addEmployee', 'removeEmployee', 'addPosition', 'removePosition']
        self.chatManagerTasks = ['sendChat']
        self.getInformation()

    # Get data from a secret file
    def getInformation(self):
        try:
            fileObject = open(self.logFileName, 'rb')
            self.companyName = pickle.load(fileObject)
            fileObject.close()
        except FileNotFoundError:
            fileObject = open(self.logFileName, 'wb')
            self.companyName = 'Company Name'
            pickle.dump(self.companyName, fileObject)
            fileObject.close()
        self.clientSocket.send(self.companyName.encode('ascii'))

    # notify All to getInitialInfo
    def notifyAll(self):
        for username in self.userManager.clientSocketList:
            try:
                clientSocket = self.userManager.clientSocketList[username]
                clientSocket.send('changeCompanyName'.encode('ascii'))
                obj = pickle.dumps(self.companyName)
                clientSocket.send(obj)
            except KeyError:
                pass

    # Constantly recieve data from the client
    def run(self):
        try:
            while True:
                task = self.clientSocket.recv(32)
                print(task)
                task = task.decode('ascii')
                if task == '':
                    pickle.loads(self.clientSocket.recv(4096))
                    break
                try:
                    obj = pickle.loads(self.clientSocket.recv(4096))
                    # Seperate task for each manager
                    if task == 'changeCompanyName':
                        self.companyName = obj
                        self.notifyAll()
                    if task in self.userManagerTasks:
                        obj = self.userManager.work(task, obj)
                        if task == 'logIn' and type(obj) == User:
                            self.currentUsername = obj.username
                            self.userManager.clientSocketList[obj.username] = self.clientSocket
                        if obj is not None:
                            self.send(task, obj)
                    elif task in self.departmentManagerTasks:
                        obj = self.departmentManager.work(task, obj)
                        if obj is not None:
                            self.send(task, obj)
                    elif task in self.chatManagerTasks:
                        obj = self.chatManager.work(task, obj)
                        if obj is not None:
                            self.send(task, obj)
                    elif task in self.projectManagerTasks:
                        obj = self.projectManager.work(task, obj)
                        if obj is not None:
                            self.send(task, obj)
                    elif task in self.eventManagerTasks:
                        obj = self.eventManager.work(task, obj)
                        if obj is not None:
                            self.send(task, obj)
                except EOFError:
                    pass
        except ConnectionResetError:
            # Completely terminate connection when the client disconnects
            if self.currentUsername is None:
                self.clientSocket.close()
                print(self.address, "disconnected")
            else:
                del self.userManager.clientSocketList[self.currentUsername]
                self.userManager.setStatus(self.currentUsername, "Offline")
                self.currentUsername = None
                self.clientSocket.close()
                print(self.address, "disconnected")

    # Send task and object to the client
    def send(self, task, obj):
        self.clientSocket.send(task.encode('ascii'))
        obj = pickle.dumps(obj)
        self.clientSocket.send(obj)