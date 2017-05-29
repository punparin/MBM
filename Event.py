from Work import *
import time

class UserAlreadyExists(Exception) : pass
class InvalidArgument(Exception) : pass

class Event(Work):
    def __init__(self, title, leaderUsername):
        super().__init__(title, leaderUsername)
        self.getCreatedDate()

    def getCreatedDate(self):
        temp = time.asctime(time.localtime(time.time())).split()
        self.createdDate = [temp[2], temp[1], temp[4]]

    def changeTitle(self, title):
        self.title = title

    def addMember(self, username):
        if self.findMember(username):
            raise UserAlreadyExists()
        self.memberList.append(username)

    def findMember(self, username):
        return username in self.memberList

    def setDueDate(self, day, month, year):
        self.dueDate = [day, month, year]

    def addLeader(self, username):
        if self.findMember(username):
            self.leader = username

    def isMemberInEvent(self, username):
        return username in self.memberList

    def removeMember(self, username):
        try:
            self.memberList.remove(username)
        except ValueError:
            raise InvalidArgument(username + " does not exists")

    def setDone(self):
        self.isDone = True

    def addText(self, text):
        self.textList.append(text)

    def addAttachment(self, attachment):
        self.attachmentList.append(attachment)