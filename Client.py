import socket


class Client:
    def __init__(self, host, port=9999):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port

    def connect(self):
        self.s.connect((self.host, self.port))
        msg = self.s.recv(1024)
        print(msg.decode('ascii'))

    def close(self):
        self.s.close()


def main():
    try:
        client = Client(socket.gethostname())
        client.connect()
        client.close()
    except OSError:
        print("Connection Failed")

if __name__ == "__main__":
    main()
