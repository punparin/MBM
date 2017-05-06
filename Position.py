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

    def hasUser(self, userID):
        try:
            self.employeeList[userID]
            return True
        except KeyError:
            return False

    def insertUser(self, user):
        try:
            user = self.employeeList[user.id]
            raise UserAlreadyExist()
        except KeyError:
            self.employeeList[user.id] = user

    def removeUser(self, userID):
        try:
            del self.employeeList[userID]
        except KeyError:
            raise UserNotFound()

    def __str__(self):
        return self.name

    def show(self, pre):
        s = self.name
        for user in self.employeeList:
            s += '\n\t\t' + ' ' * len(str(pre)) + '- ' + str(user)
        return s