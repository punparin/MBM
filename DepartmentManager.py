from Department import *

class DepartmentManager:
    def __init__(self, userManager):
        self.userManager = userManager
        self.departments = []

    def addDepartment(self, department):
        for dep in self.departments:
            if dep.name == department:
                print(department, 'already exists')
                return
        self.departments.append(Department(department))
        print('Created', department, 'successfully')

    def addEmployee(self, department, username):
        for dep in self.departments:
            if dep.name == department:
                user = self.userManager.findByUsername(username)
                if user is not None:
                    dep.addEmployee(user)
                    print('Added', username, 'to', department, 'successfully')
                else:
                    print(username, 'does not exist')
                return
        print(department, 'does not exist')