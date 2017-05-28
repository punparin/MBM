import abc

class Work(metaclass = abc.ABCMeta):
    def __init__(self, title, info):
        self.title = title
        self.contributorList = []
        self.info = info

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