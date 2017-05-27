import threading
from UserManager import *

class Handler(threading.Thread):
    def __init__(self, userManager, departmentManager, clientSocket, address):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
        self.userManager = userManager
        #self.projectManager = projectManager
        self.departmentManager = departmentManager
        self.address = address
        self.currentUsername = None
        self.userManagerTasks = ['logIn', 'register', 'updateProfile', 'getUserInfo', 'updateStatus']
        self.projectManagerTasks = ['create', 'search', 'updateProject']
        self.departmentManagerTasks = ['getInitialInfo']
        self.clientSocket.send("Connected Successfully".encode('ascii'))
        self.userManager.clientSocketList.append(self.clientSocket)

    # Constantly recieve data from the client
    def run(self):
        try:
            while True:
                task = self.clientSocket.recv(1024).decode('ascii')
                if task == '':
                    pickle.loads(self.clientSocket.recv(1024))
                    break
                try:
                    obj = pickle.loads(self.clientSocket.recv(4096))
                    # Seperate task for each manager
                    if task in self.userManagerTasks:
                        obj = self.userManager.work(task, obj)
                        if task == 'logIn' and type(obj) == User:
                            self.currentUsername = obj.username
                        if obj is not None:
                            self.send(task, obj)
                    elif task in self.departmentManagerTasks:
                        obj = self.departmentManager.work(task, obj)
                        if obj is not None:
                            self.send(task, obj)
                except EOFError:
                    pass
        except ConnectionResetError:
            # Completely terminate connection when the client disconnects
            self.userManager.clientSocketList.remove(self.clientSocket)
            self.clientSocket.close()
            print(self.address, "disconnected")
            self.userManager.setStatus(self.currentUsername, "Offline")
            self.currentUsername = None

    # Send task and object to the client
    def send(self, task, obj):
        self.clientSocket.send(task.encode('ascii'))
        obj = pickle.dumps(obj)
        self.clientSocket.send(obj)