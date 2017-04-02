import socket
from Handler import *
from UserManager import *

class Server:
    def __init__(self, port=9999):
        print("Initializing Server...")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.port = port
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        self.userManager = UserManager(self.socket)
        print("The server is ready!")

    # Waiting for connection, then send the connection to Handler
    def listen(self):
        try:
            while True:
                clientSocket, address = self.socket.accept()
                print("Got a connection from %s" % str(address))
                thread = Handler(self.userManager, clientSocket, address)
                thread.setDaemon(True)
                thread.start()
        except OSError:
            print("The port is not available")

def main():
    server = Server()
    server.listen()

if __name__ == "__main__":
    main()
