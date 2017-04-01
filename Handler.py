import pickle
import socket
import threading

class Handler(threading.Thread):
    def __init__(self, userManager, clientSocket, address):
        threading.Thread.__init__(self)
        self.userManager = userManager
        self.clientSocket = clientSocket
        self.address = address
        self.userManagerTasks = ['logIn', 'register', 'getUsers']

    def run(self):
        try:
            while True:
                print('listening')
                task = self.clientSocket.recv(1024).decode('ascii')
                try:
                    obj = pickle.loads(self.clientSocket.recv(4096))
                    #seperate task for each manager here
                    if task in self.userManagerTasks:
                        self.userManager.work(task, obj)
                except EOFError:
                    pass

        finally:
            self.clientSocket.close()