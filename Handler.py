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
        self.listen()

    def listen(self):
        try:
            while True:
                print('listening')
                task = self.clientSocket.recv(1024).decode('ascii')
                obj = pickle.loads(self.clientSocket.recv(4096))
                print('recieved')
                print(task)
                #seperate task for each manager here
                if task in self.userManagerTasks:
                    self.userManager.work(task, obj)

        finally:
            self.clientSocket.close()