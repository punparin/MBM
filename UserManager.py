import pickle
from User import *

class UserManager:
    def __init__(self, clientSocket):
        self.userListFileName = "userList"
        self.userList = []
        self.clientSocket = clientSocket
        self.getUsers()

    # Identify task for the exact function
    def work(self, task, user):
        processedObj = None
        if task == 'register':
            processedObj = self.registerUser(user)
        elif task == 'logIn':
            processedObj = self.logIn(user)
        return processedObj

    # Get all users to self.userList
    def getUsers(self):
        print("Loading users...")
        self.userList = []
        try:
            file_object = open(self.userListFileName, 'rb')
        except FileNotFoundError:
            file_object = open(self.userListFileName, 'ab')
        try:
            while True:
                obj = pickle.load(file_object)
                self.userList.append(obj)
        except EOFError:
            pass

    # Register new user
    def registerUser(self, user):
        for registeredUser in self.userList:
            if user.username == registeredUser.username:
                print(user.username + " is not available")
                return user.username + " is not available"
            if user.email == registeredUser.email:
                print(user.email + " is not available")
                return user.email + " is not available"
        credential = self.credentialValidation(user.username, user.password, user.email)
        if credential is True:
            user = User(user.username, user.password, user.email)
            fileObject = open(self.userListFileName, 'ab')
            pickle.dump(user, fileObject)
            fileObject.close()
            self.userList.append(user)
            print("Created User:", user.username, "successfully")
            return True
        else:
            print("Created User:", user.username, "failed")
            return "Your " + credential + " is not valid"

    # Log in user
    def logIn(self, user):
        for registeredUser in self.userList:
            if user.username == registeredUser.username and user.password == registeredUser.password:
                print("User:", user.username, "logged in successfully")
                return registeredUser
        print("User:", user.username, "logged in failed")
        return "User: " + user.username + " logged in failed"

    # Check whether the credentials are valid
    def credentialValidation(self, username, password, email):
        if not ('@' in email and '.' in email):
            return "email"
        isDigit = False
        isCapitalized = False
        for alp in password:
            if alp.isdigit():
                isDigit = True
            if alp.isupper():
                isCapitalized= True
        if not (isDigit and isCapitalized):
            return "password"
        for user in self.userList:
            if username == user.username or email == user.email:
                return "username"
        return True




