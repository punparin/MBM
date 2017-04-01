import pickle
from User import *

class UserManager:
    def __init__(self):
        self.userListFileName = "userList"
        self.userList = []
        self.getUsers()

    def work(self, task, user):
        if task == 'register':
            self.registerUser(user)
        elif task == 'getUsers':
            self.getUsers()
        elif task == 'logIn':
            self.logIn(user)

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

    def registerUser(self, user):
        if self.credentialValidation(user.username, user.password, user.email):
            user = User(user.username, user.password, user.email)
            fileObject = open(self.userListFileName, 'ab')
            pickle.dump(user, fileObject)
            fileObject.close()
            self.userList.append(user)
            print("Create user:", user.username, "successfully")
        else:
            print("Failed")

    def logIn(self, user):
        print(user.username, user.password)
        for registeredUser in self.userList:
            if user.username == registeredUser.username and user.password == registeredUser.password:
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




