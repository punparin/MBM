import time

class Chat:
    def __init__(self, sender, reciever):
        self.sender = sender
        self.reciever = reciever
        self.message = ""
        self.date = None
        self.time = None
        self.getTime()

    def getTime(self):
        temp = time.asctime(time.localtime(time.time())).split()
        self.date = temp[0] + " " + temp[1] + " " + temp[2] + " "  + temp[4]
        self.time = temp[3]