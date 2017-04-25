class InvalidArgument(Exception) : pass

class Department:
    departments = []
    def __init__(self, name):
        if name in self.departments:
            raise InvalidArgument('The name has already been used')
        self.name = name
        self.employees = []
        self.positionList = []
        self.subdepartment = []

    def setName(self, name):
        if name in self.departments:
            raise InvalidArgument('The name has already been used')
        self.name = name

    def addEmployee(self, user):
        self.employees.append(user)
