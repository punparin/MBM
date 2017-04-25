import pickle

class InvalidArgument(Exception) : pass

class Department:
    departments = []
    def __init__(self, name):
        if name in self.departments:
            raise InvalidArgument('The name has already been used')
        self.name = name
        #self.departmentFileName = name + 'Info'
        self.employeeIDList = []
        self.positionList = []
        self.subdepartment = []
    '''
    def getEmployees(self):
        try:
            fileObject = open(self.departmentFileName, 'rb')
        except FileNotFoundError:
            fileObject = open(self.departmentFileName, 'ab')
        try:
            while True:
                obj = pickle.load(fileObject)
                self.employeeIDList.append(obj)
        except EOFError:
            fileObject.close()

    def saveEmployee(self, employeeID):
        fileObject = open(self.departmentFileName, 'ab')
        pickle.dump(employeeID, fileObject)
        fileObject.close()
    '''
    def setName(self, name):
        if name in self.departments:
            raise InvalidArgument('The name has already been used')
        self.name = name

    def addEmployee(self, userID):
        self.employeeIDList.append(userID)
        print(self.employeeIDList)

    def __str__(self):
        s = self.name
        for employeeID in self.employeeIDList:
            s += "\n\t- " + format(employeeID, '05d')
        return s