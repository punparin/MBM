import pickle
import io
from User import *

class UserManager:
    def __init__(self):
        self.userListFileName = "userList"
        self.latestUserIDFileName = "constantID"
        self.userList = {}
        self.latestUserID = self.getLatestUserID()
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

    def getLatestUserID(self):
        latestUserID = 0
        try:
            fileObject = open(self.latestUserIDFileName, 'rb')
            latestUserID = pickle.load(fileObject)
            fileObject.close()
        except FileNotFoundError:
            fileObject = open(self.latestUserIDFileName, 'wb')
            pickle.dump(latestUserID, fileObject)
            fileObject.close()
        return latestUserID

    def saveLatestUserID(self):
        fileObject = open(self.latestUserIDFileName, 'wb')
        pickle.dump(self.latestUserID, fileObject)
        fileObject.close()

    def removeUserList(self):
        fileObject = open(self.userListFileName, 'wb')
        fileObject.close()
        self.latestUserID = 0
        fileObject = open(self.latestUserIDFileName, 'wb')
        pickle.dump(self.latestUserID, fileObject)
        fileObject.close()
        self.userList = {}
        print('Cleared successfully')

    def addAdmin(self, username):
        user = self.findByUsername(username)
        if user is None:
            print(username, 'does not exist')
        else:
            user.isAdmin = True
            self.update(user)
            print('Promoted', username, 'successfully')

    def delAdmin(self, username):
        user = self.findByUsername(username)
        if user is None:
            print(username, 'does not exist')
        else:
            if user.isAdmin:
                user.isAdmin = False
                self.update(user)
                print('Demoted', username, 'successfully')
            else:
                print(username, 'is not an admin')

    def findByUsername(self, username):
        try:
            return self.userList[username]
        except KeyError:
            return None

    def setStatus(self, username, status):
        user = self.findByUsername(username)
        if user is None:
            print(username, 'is not an admin')
        else:
            user.status = status
            # notify all

    def showUserList(self):
        for username in self.userList:
            print(self.userList[username])

    def findUserByUsername(self, username):
        user = self.findByUsername(username)
        if user is not None:
            print(user)
        else:
            print(username, "not found")

    # Get all users to self.userList
    def getUsers(self):
        print("Loading users...")
        self.userList = {}
        try:
            fileObject = open(self.userListFileName, 'rb')
        except FileNotFoundError:
            fileObject = open(self.userListFileName, 'ab')
        try:
            while True:
                obj = pickle.load(fileObject)
                self.userList[obj.username] = obj
        except EOFError:
            fileObject.close()
        except (AttributeError, io.UnsupportedOperation):
            fileObject.close()

    # Register new user
    def registerUser(self, user):
        for username in self.userList:
            registeredUser = self.userList[username]
            if user.username == registeredUser.username:
                print(user.username + " is unavailable")
                return user.username + " is unavailable"
            if user.email == registeredUser.email:
                print(user.email + " is unavailable")
                return user.email + " is unavailable"
        credential = self.credentialValidation(user.username, user.password, user.email)
        if credential is True:
            self.latestUserID += 1
            user = User(user.username.lower(), user.password, user.email.lower())
            user.id = self.latestUserID
            self.userList[user.username] = user
            self.saveUser(user)
            self.saveLatestUserID()
            print("Created User:", user.username, "successfully")
            return True
        else:
            print("Created User:", user.username, "failed")
            return "Your " + credential + " is invalid"

    def removeUser(self, username):
        user = self.findByUsername(username)
        if user is not None:
            del self.userList[username]
            self.saveUsers()
            print("Removed", username, "successfully")
        else:
            print(username, "does not exist")

    # Log in user
    def logIn(self, user):
        registeredUser = self.findByUsername(user.username)
        if registeredUser is None:
            print("User:", user.username, "logged in fail")
            return "User: " + user.username + " logged in fail"
        elif user.username == registeredUser.username and user.password == registeredUser.password:
            print("User:", user.username, "logged in successfully")
            return registeredUser
        else:
            print("User:", user.username, "logged in fail")
            return "User: " + user.username + " logged in fail"

    #update user
    def update(self, user):
        self.userList[user.username] = user
        self.saveUsers()

    def saveUser(self, user):
        fileObject = open(self.userListFileName, 'ab')
        pickle.dump(user, fileObject)
        fileObject.close()

    def saveUsers(self):
        fileObject = open(self.userListFileName, 'wb')
        for username in self.userList:
            pickle.dump(self.userList[username], fileObject)
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
                isCapitalized = True
        if not (isDigit and isCapitalized):
            return "password"
        return True




