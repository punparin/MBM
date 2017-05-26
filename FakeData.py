from UserManager import *
from DepartmentManager import *

curNum = 1
userManager = UserManager()
departmentManager = DepartmentManager(userManager)

def createUser(username):
    global curNum
    user = User(username + str(curNum), 'Admin1234', username + str(curNum) + '@gmail.com')
    user.id = curNum
    curNum += 1
    return user

def generateFakeUser(n):
    for i in range(n):
        user = createUser('test')
        userManager.registerUser(user)

def removeUserList():
    userManager.removeUserList()

def removeDepartmentList():
    departmentManager.removeDepartmentList()

def createPunparin():
    user = User('punparin', 'Pun1234', 'punparin@gmail.com')
    userManager.registerUser(user)

def createDepartment():
    departmentManager.addDepartment('Dev')
    departmentManager.addPosition('Dev', 'Manager')
    departmentManager.addPosition('Dev', 'SeniorDev', 'Manager')
    departmentManager.addPosition('Dev', 'JuniorDev', 'SeniorDev')
    departmentManager.addEmployee('Dev', 'Manager', 'punparin')
    departmentManager.addEmployee('Dev', 'SeniorDev', 'test1')
    departmentManager.addEmployee('Dev', 'JuniorDev', 'test2')

if __name__ == "__main__":
    removeUserList()
    removeDepartmentList()
    createPunparin()
    generateFakeUser(2)
    createDepartment()
    userManager.getUserInfo('punparin')
    userManager.getUserStatus('punparin')
    departmentManager.getInitialInfo()