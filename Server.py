import socket


class Server:
    def __init__(self, port=9999):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.port = port
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)

    def listen(self):
        try:
            while True:
                client_socket, addr = self.socket.accept()
                print("Got a connection from %s" % str(addr))
                msg = "Connected Successfully"
                client_socket.send(msg.encode('ascii'))
        finally:
            client_socket.close()


def main():
    try:
        server = Server()
        server.listen()
    except OSError:
        print("The port is not available")

if __name__ == "__main__":
    main()
