from Department import *

class DepartmentManager:
    def __init__(self, userManager):
        self.departmentFileName = 'departmentList'
        self.userManager = userManager
        self.departmentList = []
        self.getDepartments()

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

    def addDepartment(self, department):
        for dep in self.departmentList:
            if dep.name == department:
                print(department, 'already exists')
                return
        dep = Department(department)
        self.departmentList.append(dep)
        self.saveDepartment(dep)
        print('Created', department, 'successfully')

    def addSubDepartment(self, department, subdepartment):
        dep = None
        subdep = None
        for temp in self.departmentList:
            if temp.name == department:
                dep = temp
            elif temp.name == subdepartment:
                subdep = temp
        if dep is None:
            print(department, 'does not exist')
        if subdep is None:
            print(subdepartment, 'does not exist')
        if dep is not None and subdep is not None:
            if subdep.hasSubdepartment(dep):
                print(department, 'is a subdepartment of', subdepartment, ', Please remove', department, 'from subdepartment of', subdep, 'before adding it')
            else:
                dep.addSubdepartment(subdep)
                self.saveDepartments()
                print('Added', subdepartment, 'to', department, 'successfully')

    def addEmployee(self, department, username):
        for dep in self.departmentList:
            if dep.name == department:
                user = self.userManager.findByUsername(username)
                if user is not None:
                    dep.addEmployee(user.id)
                    self.saveDepartments()
                    print('Added', username, 'to', department, 'successfully')
                else:
                    print(username, 'does not exist')
                return
        print(department, 'does not exist')

    def showDepartment(self):
        for department in self.departmentList:
            print('-', department)