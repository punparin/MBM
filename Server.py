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
        self.userManager = UserManager()
        print("The server is ready!")

    def listen(self):
        try:
            while True:
                clientSocket, address = self.socket.accept()
                print("Got a connection from %s" % str(address))
                msg = "Connected Successfully"
                clientSocket.send(msg.encode('ascii'))
                thread = Handler(self.userManager, clientSocket, address)
                thread.start()
        except OSError:
            print("The port is not available")


def main():
    server = Server()
    server.listen()

if __name__ == "__main__":
    main()
