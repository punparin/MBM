import socket
from Handler import *
from UserManager import *
from ProjectManager import *

class Server:
    def __init__(self, port=9999, maximumClient = 10):
        print("Initializing Server...")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.port = port
        self.maximumClient = maximumClient
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(self.maximumClient)
            self.userManager = UserManager(self.socket)
            self.projectManager = ProjectManager(self.socket)
            print("The server is ready!")
            self.listen()
        except OSError:
            print("Server is already working!")

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
