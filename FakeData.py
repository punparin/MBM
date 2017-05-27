from UserManager import *
from elizabeth import *
from DepartmentManager import *

curNum = 1
userManager = UserManager()
departmentManager = DepartmentManager(userManager)

def createUser(username):
    global curNum
    p = Personal
    user = User(username + str(curNum), 'Admin1234', username + str(curNum) + '@gmail.com')
    user.name = p.name
    user.last_name = p.surname
    user.id = curNum
    curNum += 1
    return user

def generateFakeUser(title, n):
    for i in range(n):
        user = createUser(title)
        userManager.registerUser(user)

def removeUserList():
    userManager.removeUserList()

def removeDepartmentList():
    departmentManager.removeDepartmentList()

def createPunparin():
    user = User('punparin', 'Pun1234', 'punparin@gmail.com')
    user.name = 'Parin'
    user.last_name = 'Kobboon'
    userManager.registerUser(user)

def createAdmin():
    user = User('admin', 'Admin1234', 'admin@gmail.com')
    user.name = 'Admin'
    user.last_name = 'Eiei'
    userManager.registerUser(user)

def createDepartment():
    departmentManager.addDepartment('Dev')
    departmentManager.addPosition('Dev', 'Manager')
    departmentManager.addPosition('Dev', 'SeniorDev', 'Manager')
    departmentManager.addPosition('Dev', 'JuniorDev', 'SeniorDev')
    departmentManager.addPosition('Dev', 'SeniorTester', 'Manager')
    departmentManager.addPosition('Dev', 'JuniorTester', 'SeniorTester')
    departmentManager.addEmployee('Dev', 'Manager', 'punparin')
    departmentManager.addEmployee('Dev', 'SeniorDev', 'test1')
    departmentManager.addEmployee('Dev', 'JuniorDev', 'test2')
    departmentManager.addEmployee('Dev', 'SeniorDev', 'test3')
    departmentManager.addEmployee('Dev', 'JuniorDev', 'test4')
    departmentManager.addDepartment('HR')
    departmentManager.addPosition('HR', 'Manager')
    departmentManager.addPosition('HR', 'SeniorHR', 'Manager')
    departmentManager.addPosition('HR', 'JuniorHR', 'SeniorHR')
    departmentManager.addEmployee('HR', 'Manager', 'test5')
    departmentManager.addEmployee('HR', 'SeniorHR', 'test6')
    departmentManager.addEmployee('HR', 'JuniorHR', 'test7')

if __name__ == "__main__":
    removeUserList()
    removeDepartmentList()
    createPunparin()
    createAdmin()
    generateFakeUser('test', 7)
    createDepartment()
    userManager.getUserInfo('punparin')
    userManager.getUserStatus('punparin')
    generateFakeUser('admin', 3)