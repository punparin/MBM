import time

class Chat:
    def __init__(self, sender, reciever):
        self.sender = sender
        self.reciever = reciever
        self.message = ""
        self.date = None
        self.time = None
        self.getDateTime()

    def getDateTime(self):
        temp = time.asctime(time.localtime(time.time())).split()
        self.date = [temp[2], temp[1], temp[4]]
        self.time = temp[3]