from Work import *

class UserAlreadyExists(Exception) : pass
class InvalidArgument(Exception) : pass

class Project(Work):
    def __init__(self, title, department, info = None):
        super().__init__(title, department, info)
        self.tasks = []
        self.leader = ""

    def changeTitle(self, title):
        self.title = title

    def addContributor(self, username):
        if self.findContributor(username):
            raise UserAlreadyExists()
        self.contributorList.append(username)

    def addLeader(self, username):
        if self.findContributor(username):
            self.leader = username

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

    def setDone(self):
        self.isDone = True

    def addTask(self, task):
        if task not in self.tasks:
            self.tasks.append(task)