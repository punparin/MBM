class UserNotFound(Exception) : pass
class UserAlreadyExist(Exception) : pass

class Position:
    def __init__(self, name):
        self.name = name
        self.employeeList = {}
        self.canUseProject = True
        self.canUseEvent = True
        self.canCreateProject = True
        self.canCreateEvent = True
        self.canJoinEvent = True
        self.canJoinProject = True

    def getPerMissionList(self):
        return [self.canUseProject,self.canUseEvent ,self.canCreateProject, self.canCreateEvent, self.canJoinEvent, self.canJoinProject]

    def hasUser(self, userID):
        try:
            self.employeeList[userID]
            return True
        except KeyError:
            return False

    def insertUser(self, userID, username):
        try:
            self.employeeList[userID]
            raise UserAlreadyExist()
        except KeyError:
            self.employeeList[userID] = username

    def removeUser(self, userID):
        try:
            del self.employeeList[userID]
        except KeyError:
            raise UserNotFound()

    def __str__(self):
        return self.name

    def show(self, pre):
        s = self.name
        for key in self.employeeList:
            s += '\n\t\t' + ' ' * len(str(pre)) + '- ' + format(key, '05d') + ": " + self.employeeList[key]
        return s