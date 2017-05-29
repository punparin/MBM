import abc

class Work(metaclass = abc.ABCMeta):
    def __init__(self, title, leaderUsername):
        self.title = title
        self.leader = leaderUsername
        self.memberList = []
        self.description = ""
        self.textList = []
        self.attachmentList = []
        self.status = "Not Started"
        self.createdDate = ""
        self.dueDate = None

    @abc.abstractmethod
    def getCreatedDate(self):
        pass

    @abc.abstractmethod
    def changeTitle(self, title):
        pass

    @abc.abstractmethod
    def addMember(self, username):
        pass

    @abc.abstractmethod
    def findMember(self, username):
        pass

    @abc.abstractmethod
    def removeMember(self, username):
        pass

    @abc.abstractmethod
    def addLeader(self, username):
        pass

    @abc.abstractmethod
    def setDone(self):
        pass

    @abc.abstractmethod
    def setDueDate(self, day, month, year):
        pass

    @abc.abstractmethod
    def addText(self, text):
        pass

    @abc.abstractmethod
    def addAttachment(self, attachment):
        pass