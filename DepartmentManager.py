import pickle
from Department import *

class DepartmentManager:
    def __init__(self, userManager):
        self.departmentFileName = 'departmentList'
        self.userManager = userManager
        self.departmentList = []
        self.getDepartments()

    def addPosition(self, department, position, parent = None):
        for dep in self.departmentList:
            if dep.name == department:
                try:
                    dep.addPosition(position, parent)
                    print("Added", position, "successfully")
                    self.saveDepartments()
                except InvalidArgument as err:
                    print(err)
                break

    def removePosition(self, department, position):
        pass

    def getDepartments(self):
        print("\nLoading departments...")
        try:
            fileObject = open(self.departmentFileName, 'rb')
        except FileNotFoundError:
            fileObject = open(self.departmentFileName, 'ab')
        try:
            while True:
                obj = pickle.load(fileObject)
                print("\n- " + str(obj))
                self.departmentList.append(obj)
        except EOFError:
            fileObject.close()

    def saveDepartment(self, department):
        fileObject = open(self.departmentFileName, 'ab')
        pickle.dump(department, fileObject)
        fileObject.close()

    def saveDepartments(self):
        fileObject = open(self.departmentFileName, 'wb')
        for department in self.departmentList:
            pickle.dump(department, fileObject)
        fileObject.close()

    def removeDepartment(self, department):
        dep = None
        for temp in self.departmentList:
            if temp.name == department:
                dep = temp
        if dep is None:
            print(department, 'does not exist')
        else:
            for temp in self.departmentList:
                if temp.hasSubdepartment(dep.name):
                    temp.removeSubdepartment(dep.name)
            self.departmentList.remove(dep)
            self.saveDepartments()
            print('Removed', department, 'successfully')

    def addDepartment(self, department):
        for dep in self.departmentList:
            if dep.name == department:
                print(department, 'already exists')
                return
        dep = Department(department)
        self.departmentList.append(dep)
        self.saveDepartment(dep)
        print('Created', department, 'successfully')

    def addEmployee(self, department, position, username):
        for dep in self.departmentList:
            if dep.name == department:
                user = self.userManager.findByUsername(username)
                if user is not None:
                    dep.addEmployee(position, user)
                    self.saveDepartments()
                    print('Added', username, 'to', department, 'successfully')
                else:
                    print(username, 'does not exist')
                return
        print(department, 'does not exist')

    def showDepartment(self):
        for department in self.departmentList:
            print('-', department)