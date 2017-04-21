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
        elif task == 'updateProfile':
            self.update(user)
        return processedObj

    def addAdmin(self, username):
        for user in self.userList:
            if user.username == username:
                user.isAdmin = True
                print('Promoted', username, 'to be admin successfully')
                return
        print(username, 'does not exist')

    # Get all users to self.userList
    def getUsers(self):
        print("Loading users...")
        self.userList = []
        try:
            fileObject = open(self.userListFileName, 'rb')
        except FileNotFoundError:
            fileObject = open(self.userListFileName, 'ab')
        try:
            while True:
                obj = pickle.load(fileObject)
                self.userList.append(obj)
        except EOFError:
            fileObject.close()

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

    #update user
    def update(self, user):
        for i in range(len(self.userList)):
            if user.username == self.userList[i].username:
                self.userList[i] = user
        self.saveUsers()

    def saveUsers(self):
        fileObject = open(self.userListFileName, 'wb')
        for registeredUser in self.userList:
            pickle.dump(registeredUser, fileObject)
        fileObject.close()

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




