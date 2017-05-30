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
        self.userManagerTasks = ['logIn', 'register', 'updateProfile', 'getUserInfo', 'updateStatus']
        self.projectManagerTasks = ['createProject', 'searchProject', 'updateProject', 'removeProject', 'getInitialProject']
        self.eventManagerTasks = ['createEvent', 'searchEvent', 'updateEvent', 'removeEvent', 'getInitialEvent']
        self.departmentManagerTasks = ['getInitialInfo']
        self.chatManagerTasks = ['sendChat']
        self.clientSocket.send("Connected Successfully".encode('ascii'))

    # Constantly recieve data from the client
    def run(self):
        try:
            while True:
                task = self.clientSocket.recv(32).decode('ascii')
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