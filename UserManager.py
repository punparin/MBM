import pickle
from User import *

class UserManager:
    def __init__(self):
        self.userListFileName = "userList"
        self.userList = []
        self.getUsers()

    def work(self, task, obj):
        if task == 'register':
            self.registerUser(obj[0], obj[1], obj[2])
        elif task == 'getUsers':
            self.getUsers()
        elif task == 'logIn':
            self.logIn(obj[0], obj[1])

    def getUsers(self):
        self.userList = []
        try:
            file_object = open(self.userListFileName, 'rb')
        except FileNotFoundError:
            open(self.userListFileName, 'ab')
        try:
            while True:
                obj = pickle.load(file_object)
                self.userList.append(obj)
                print(obj)
        except EOFError:
            pass

    def registerUser(self, username, password, email):
        if self.credentialValidation(username, password, email):
            user = User(username, password, email)
            fileObject = open(self.userListFileName, 'ab')
            pickle.dump(user, fileObject)
            fileObject.close()
            self.userList.append(user)
            print("Create user:", username, "successfully")
        else:
            print("Failed")

    def logIn(self, username, password):
        print(username, password)
        for user in self.userList:
            if username == user.username and password == user.password:
                print("Logged In")
                return
        print("Failed")

    def credentialValidation(self, username, password, email):
        if not ('@' in email and '.' in email):
            return False
        isDigit = False
        isCapitalized = False
        for alp in password:
            if alp.isdigit():
                isDigit = True
            if alp.isupper():
                isCapitalized= True
        if not (isDigit and isCapitalized):
            return False
        for user in self.userList:
            if username == user.username or email == user.email:
                return False
        return True




