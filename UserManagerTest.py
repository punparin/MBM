import sys
import unittest
from io import StringIO
from UserManager import *
from elizabeth import *

class UserManagerTest(unittest.TestCase):
    def setUp(self):
        self.held, sys.stdout = sys.stdout, StringIO()
        self.userManager = UserManager()
        self.userManager.removeUserList()
        self.initOutput = sys.stdout.getvalue().strip()
        self.curNum = 1

    def getLatestOutput(self):
        output = sys.stdout.getvalue().strip().replace(self.initOutput, '')[1:]
        self.initOutput = sys.stdout.getvalue().strip()
        return output

    def createUser(self, username):
        user = User(username + str(self.curNum), 'Admin1234', username + str(self.curNum) + '@gmail.com')
        user.id = self.curNum
        self.curNum += 1
        return user

    def test_registerUser(self):
        # success
        user = User('admin', 'Admin1234', 'admin@gmail.com')
        self.userManager.registerUser(user)
        self.assertEqual("Created User: admin successfully", self.getLatestOutput())
        # unavailable username
        user = User('admin', 'Admin1234', 'admin1@gmail.com')
        self.userManager.registerUser(user)
        self.assertEqual("admin is unavailable", self.getLatestOutput())
        # unavailable email
        user = User('admin1', 'Admin1234', 'admin@gmail.com')
        self.userManager.registerUser(user)
        self.assertEqual("admin@gmail.com is unavailable", self.getLatestOutput())
        # invalid password
        user = User('admin1', 'admin1234', 'admin1@gmail.com')
        self.userManager.registerUser(user)
        self.assertEqual("Created User: admin1 failed", self.getLatestOutput())
        # invalid email
        user = User('admin1', 'admin1234', 'admin1gmailcom')
        self.userManager.registerUser(user)
        self.assertEqual("Created User: admin1 failed", self.getLatestOutput())
        # success
        user = User('admin1', 'Admin1234', 'admin1@gmail.com')
        self.userManager.registerUser(user)
        self.assertEqual("Created User: admin1 successfully", self.getLatestOutput())

    def test_logInUser(self):
        # success
        user = User('admin', 'Admin1234', 'admin@gmail.com')
        self.userManager.registerUser(user)
        self.getLatestOutput()
        self.userManager.logIn(user)
        self.assertEqual("User: admin logged in successfully", self.getLatestOutput())
        # failed non-existent user
        user = User('admin1', 'Admin1234')
        self.userManager.logIn(user)
        self.assertEqual("User: admin1 logged in fail", self.getLatestOutput())
        # failed invalid password
        user = User('admin', 'Test1234')
        self.userManager.logIn(user)
        self.assertEqual("User: admin logged in fail", self.getLatestOutput())
        # failed invalid password

    def test_removeUser(self):
        # register 100 users into the system
        userList = []
        for i in range(100):
            user = self.createUser('admin')
            userList.append(user)
            self.userManager.registerUser(user)
        self.getLatestOutput()
        # remove non-existent users
        p = Personal()
        for i in range(100):
            username = p.username()
            self.userManager.removeUser(username)
            self.assertEqual(username + ' does not exist', self.getLatestOutput())
        # remove existent users
        for user in userList:
            self.userManager.removeUser(user.username)
            self.assertEqual("Removed " + user.username + " successfully", self.getLatestOutput())
        # find removed users
        for user in userList:
            self.userManager.findUserByUsername(user.username)
            self.assertEqual(user.username + ' not found', self.getLatestOutput())

    def test_findUserByUsername(self):
        # register 100 users into the system
        userList = []
        for i in range(100):
            user = self.createUser('admin')
            userList.append(user)
            self.userManager.registerUser(user)
        self.getLatestOutput()
        # find non-existent users
        p = Personal()
        for i in range(100):
            username = p.username()
            self.userManager.findUserByUsername(username)
            self.assertEqual(username + ' not found', self.getLatestOutput())
        # find existent users
        for user in userList:
            self.userManager.findUserByUsername(user.username)
            self.assertEqual(str(user), self.getLatestOutput())

if __name__ == "__main__":
    unittest.main()