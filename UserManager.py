import pickle
from User import *

class UserManager:
    def __init__(self):
        self.userListFileName = "userList"
        self.userList = []

    def work(self, task, obj):
        if task == 'register':
            self.createUser(obj[0], obj[1], obj[2])
        elif task == 'getUsers':
            self.__getUsers()

    def __getUsers(self):
        file_object = open(self.userListFileName, 'rb')
        try:
            while True:
                obj = pickle.load(file_object)
                print(obj)
        except EOFError:
            pass

    def createUser(self, username, password, email):
        user = User()
        isValid = user.register(username, password, email)
        if isValid:
            fileObject = open(self.userListFileName, 'ab')
            pickle.dump(user, fileObject)
            fileObject.close()
            print("Create user:", username, "successfully")
        else:
            print("Failed")



