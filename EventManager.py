import pickle
import io
import copy
from Project import *
from Event import *

class EventManager:
    def __init__(self, userManager, departmentManager):
        self.eventListFileName = "eventList"
        self.userManager = userManager
        self.departmentManager = departmentManager
        self.eventList = {}
        self.getEvents()

    # Identify task for the exact function
    def work(self, task, obj):
        processedObj = None
        if task == 'createEvent':
            self.createEvent(obj)
        elif task == 'searchEvent':
            processedObj = self.searchEvent(obj)
        elif task == 'updateEvent':
            self.update(obj)
        elif task == 'removeEvent':
            self.removeEvent(obj)
        elif task == 'getInitialEvent':
            processedObj = self.getInitialEvent()
        return processedObj

    def getInitialEvent(self):
        return self.eventList

    # Get all users to self.userList
    def getEvents(self):
        print("Loading events...")
        self.eventList = {}
        try:
            fileObject = open(self.eventListFileName, 'rb')
        except FileNotFoundError:
            fileObject = open(self.eventListFileName, 'ab')
        try:
            while True:
                obj = pickle.load(fileObject)
                self.eventList[obj.title] = obj
        except EOFError:
            fileObject.close()
        except (AttributeError, io.UnsupportedOperation):
            fileObject.close()

    # Create a new event
    def createEvent(self, event):
        for title in self.eventList:
            if event.title == self.eventList[title].title:
                return
        fileObject = open(self.eventListFileName, 'ab')
        pickle.dump(event, fileObject)
        fileObject.close()
        self.eventList[event.title] = event
        self.saveEvent(event)

    # Remove a event
    def removeEvent(self, eventTitle):
        try:
            del self.eventList[eventTitle]
            self.saveEvents()
            self.notifyAll()
        except KeyError:
            return 'not found'

    # Find a event by its title
    def findByTitle(self, title):
        try:
            return self.eventList[title]
        except KeyError:
            return None

    # Search for a event
    def searchEvent(self, eventTitle):
        event = self.findByTitle(eventTitle)
        if event is not None:
            print("Event: ", event.title, "Project Found")
            return event
        else:
            print("Event: ", event.title, "Project Not Found")
            return None

    '''
    # Add a member to a project
    def addMember(self, projectTitle, username):
        project = self.searchProject(projectTitle)
        if project is not None:
            permission = self.departmentManager.getUserPermission(username)
            try:
                permission = permission[project.department]
                if permission['canCreateProject']:
                    project.addContributor(username)
                    self.update(project)
            except KeyError:
                return False

    # Remove a member from a project
    def removeMember(self, projectTitle, username):
        project = self.searchProject(projectTitle)
        if project is not None:
            try:
                project.removeMember(username)
                self.update(project)
            except InvalidArgument:
                return False
    '''

    # notify All to getInitialEvent
    def notifyAll(self, event = None):
        for username in self.userManager.clientSocketList:
            try:
                clientSocket = self.userManager.clientSocketList[username]
                if event is None:
                    clientSocket.send('getInitialEvent'.encode('ascii'))
                    obj = pickle.dumps(self.getInitialEvent())
                else:
                    clientSocket.send('updateEvent'.encode('ascii'))
                    obj = pickle.dumps(event)
                clientSocket.send(obj)
            except KeyError:
                pass

    # Update event
    def update(self, event):
        for i in range(len(self.eventList)):
            if event.title == self.eventList[i].title:
                self.eventList[i] = event
        self.saveEvents()
        # notify all to getInitialEvent
        self.notifyAll(event)

    # Save event
    def saveEvent(self, event):
        fileObject = open(self.eventListFileName, 'ab')
        pickle.dump(event, fileObject)
        fileObject.close()

    # Save all events
    def saveEvents(self):
        fileObject = open(self.eventListFileName, 'wb')
        for title in self.eventList:
            pickle.dump(self.eventList[title], fileObject)
        fileObject.close()