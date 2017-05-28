import abc

class Work(metaclass = abc.ABCMeta):
    def __init__(self, title, department, info):
        self.title = title
        self.department = department
        self.contributorList = []
        self.info = info
        self.isDone = False
        self.progress = 0

    @abc.abstractmethod
    def changeTitle(self, title):
        pass

    @abc.abstractmethod
    def addContributor(self, username):
        pass

    @abc.abstractmethod
    def findContributor(self, username):
        pass

    @abc.abstractmethod
    def removeContributor(self, username):
        pass

    @abc.abstractmethod
    def update(self, newInfo):
        pass

    @abc.abstractmethod
    def updateProgress(self, progress):
        pass

    @abc.abstractmethod
    def setDone(self):
        pass