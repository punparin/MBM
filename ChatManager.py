import pickle
from Chat import *

class ChatManager:
    def __init__(self, userManager):
        self.userManager = userManager

    def work(self, task, obj = None):
        if task == 'sendChat':
            self.sendChat(obj)

    def sendChat(self, chat):
        try:
            obj = pickle.dumps(['recieveChat', chat])
            self.userManager.clientSocketList[chat.reciever].send(obj)
        except KeyError as err:
            print(err)
