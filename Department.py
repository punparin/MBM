import pickle

class InvalidArgument(Exception) : pass

class Department:
    departments = []
    def __init__(self, name):
        if name in self.departments:
            raise InvalidArgument('The name has already been used')
        self.name = name
        self.employeeIDList = []
        self.positionList = []
        self.subdepartmentList = []

    def setName(self, name):
        if name in self.departments:
            raise InvalidArgument('The name has already been used')
        self.name = name

    def addEmployee(self, userID):
        self.employeeIDList.append(userID)

    def addSubdepartment(self, subdepartment):
        self.subdepartmentList.append(subdepartment)

    def removeSubdepartment(self, subdepartmentName):
        for subdepartment in self.subdepartmentList:
            if subdepartment.name == subdepartmentName:
                self.subdepartmentList.remove(subdepartment)

    def hasSubdepartment(self, subdepartmentName):
        for subdepartment in self.subdepartmentList:
            if subdepartment.name == subdepartmentName:
                return True
        return False

    def __str__(self):
        s = self.name
        if len(self.employeeIDList) != 0:
            s += '\nEmployees:'
        for employeeID in self.employeeIDList:
            s += "\n\t- " + format(employeeID, '05d')
        if len(self.subdepartmentList) != 0:
            s += '\nSubdepartments:'
        for subdepartment in self.subdepartmentList:
            s += "\n\t- " + subdepartment.name
        return s