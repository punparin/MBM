class UserNotFound(Exception) : pass

class Position:
    def __init__(self, name):
        self.name = name
        self.employeeList = []
        self.canUseProject = True
        self.canUseEvent = True
        self.canCreateProject = True
        self.canCreateEvent = True
        self.canJoinEvent = True
        self.canJoinProject = True

    def __insertUser(self, userID, low, high):
        mid = (low + high) // 2
        if low > high:
            return low
        if userID == self.employeeList[mid].id:
            return mid
        elif userID < self.employeeList[mid].id:
            return self.__insertUser(userID, low, mid - 1)
        else:
            return self.__insertUser(userID, mid + 1, high)

    def hasUser(self, userID):
        if len(self.employeeList) == 0:
            return False
        elif userID < self.employeeList[0].id:
            return False
        elif userID > self.employeeList[len(self.employeeList) - 1].id:
            return False
        index = self.searchUserIndex(userID, 0, len(self.employeeList))
        if index is None:
            return False
        return True

    def searchUserIndex(self, userID, low, high):
        mid = (low + high) // 2
        if low > high:
            return None
        if userID == self.employeeList[mid].id:
            return mid
        elif userID < self.employeeList[mid].id:
            return self.searchUserIndex(userID, low, mid - 1)
        else:
            return self.searchUserIndex(userID, mid + 1, high)

    def insertUser(self, user):
        if len(self.employeeList) == 0:
            self.employeeList.append(user)
        elif user.id > self.employeeList[len(self.employeeList) - 1].id:
            self.employeeList.append(user)
        elif user.id < self.employeeList[0].id:
            self.employeeList.insert(0, user)
        else:
            index = self.__insertUser(user.id, 0, len(self.employeeList))
            self.employeeList.insert(index, user)

    def removeUser(self, userID):
        if len(self.employeeList) == 0:
            raise UserNotFound(userID, "does not exist in", self.name)
        elif userID < self.employeeList[0].id:
            raise UserNotFound(userID, "does not exist in", self.name)
        elif userID > self.employeeList[len(self.employeeList) - 1].id:
            raise UserNotFound(userID, "does not exist in", self.name)
        index = self.searchUserIndex(userID, 0, len(self.employeeList))
        if index is None:
            raise UserNotFound(userID, "does not exist in", self.name)
        self.employeeList.pop(index)

    def __str__(self):
        return self.name

    def show(self, pre):
        s = self.name
        for user in self.employeeList:
            s += '\n\t\t' + ' ' * len(str(pre)) + '- ' + str(user)
        return s