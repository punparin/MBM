import socket
import pickle
from User import *

class Client:
    def __init__(self, host, port=9999):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port

    def connect(self):
        self.s.connect((self.host, self.port))
        msg = self.s.recv(1024)
        print(msg.decode('ascii'))

    def send(self, task, obj):
        self.s.send(task.encode('ascii'))
        obj = pickle.dumps(obj)
        self.s.send(obj)

    def close(self):
        self.s.close()

'''
def main():
    try:
        client = Client(socket.gethostname())
        client.connect()
        while True:
            task = input()
            if task == 'logIn':
                username, password = input().split()
                user = User(username, password)
                client.send(task, user)
            elif task == 'register':
                username, password, email = input().split()
                user = User(username, password, email)
                client.send(task, user)
            print("Sent")
        client.close()
    except OSError:
        print("Connection Failed")

if __name__ == "__main__":
    main()
'''