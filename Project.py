from Work import *

class UserAlreadyExists(Exception) : pass
class InvalidArgument(Exception) : pass

class Project(Work):
    def __init__(self, title, info = None):
        super().__init__()
        self.title = title
        self.info = info
        self.progress = 0

    def changeTitle(self, title):
        self.title = title

    def addContributor(self, username):
        if self.findContributor(username):
            raise UserAlreadyExists()
        self.contributorList.append(username)

    def findContributor(self, username):
        return username in self.contributorList

    def removeContributor(self, username):
        try:
            self.contributorList.remove(username)
        except ValueError:
            raise InvalidArgument(username + " does not exists")

    def update(self, newInfo):
        self.info = newInfo

    def updateProgress(self, progress):
        self.progress = progress