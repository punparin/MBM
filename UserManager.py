import pickle
from User import *

class UserManager:
    def __init__(self, clientSocket):
        self.userListFileName = "userList"
        self.latestUserIDFileName = "constantID"
        self.userList = []
        self.latestUserID = self.getLatestUserID()
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

    def addAdmin(self, username):
        for user in self.userList:
            if user.username == username:
                user.isAdmin = True
                print('Promoted', username, 'successfully')
                return
        print(username, 'does not exist')

    def delAdmin(self, username):
        for user in self.userList:
            if user.username == username:
                user.isAdmin = False
                print('demoted', username, 'successfully')
                return
        print(username, 'does not exist')

    # Search using brute-force approach
    def findByUsername(self, username):
        for user in self.userList:
            if user.username == username:
                return user
        return None

    def setStatus(self, userID, status):
        user = self.findByID(userID)
        if user is not None:
            user.status = status
            #notify all

    def showUserList(self):
        for user in self.userList:
            if user.isActivated:
                print(user)

    def findUserByUsername(self, username):
        user = self.findByUsername(username)
        if user is not None and user.isActivated:
            print(user)
        else:
            print(username, "not found")

    # Search by Index
    def findUserByID(self, id):
        try:
            id = int(id) - 1
            try:
                user = self.userList[id]
                if not user.isActivated:
                    print("Invalid ID1")
                else:
                    print(user)
            except IndexError:
                print("Invalid ID2")
        except ValueError:
            print("Invalid ID3")

    # Get all users to self.userList
    def getUsers(self):
        print("\nLoading users...")
        self.userList = []
        try:
            fileObject = open(self.userListFileName, 'rb')
        except FileNotFoundError:
            fileObject = open(self.userListFileName, 'ab')
        try:
            while True:
                obj = pickle.load(fileObject)
                print("- " + str(obj))
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
            self.latestUserID += 1
            user = User(user.username, user.password, user.email)
            user.id = self.latestUserID
            self.saveUser(user)
            self.userList.append(user)
            self.saveLatestUserID()
            print("Created User:", user.username, "successfully")
            return True
        else:
            print("Created User:", user.username, "failed")
            return "Your " + credential + " is not valid"

    def removeUser(self, username):
        user = self.findByUsername(username)
        if user is not None:
            user.isActivated = False
            self.saveUsers()
            print("Removed", username, "successfully")
        else:
            print(username, "not found")

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

    def saveUser(self, user):
        fileObject = open(self.userListFileName, 'ab')
        pickle.dump(user, fileObject)
        fileObject.close()

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




