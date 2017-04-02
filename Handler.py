import threading
from UserManager import *

class Handler(threading.Thread):
    def __init__(self, userManager, clientSocket, address):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
        self.userManager = userManager
        self.address = address
        self.userManagerTasks = ['logIn', 'register']
        msg = "Connected Successfully"
        self.clientSocket.send(msg.encode('ascii'))

    # Constantly recieve data from the client
    def run(self):
        try:
            while True:
                task = self.clientSocket.recv(1024).decode('ascii')
                if task == '':
                    break
                try:
                    obj = pickle.loads(self.clientSocket.recv(4096))
                    # Seperate task for each manager
                    if task in self.userManagerTasks:
                        obj = self.userManager.work(task, obj)
                        if obj is not None:
                            self.send(task, obj)
                except EOFError:
                    pass
        except ConnectionResetError:
            # Completely terminate connection when the client disconnects
            self.clientSocket.close()
            print(self.address, "disconnected")

    # Send task and object to the client
    def send(self, task, obj):
        self.clientSocket.send(task.encode('ascii'))
        obj = pickle.dumps(obj)
        self.clientSocket.send(obj)