import pickle
from Event import *

class EventManager:
    def __init__(self, clientSocket):
        self.eventListFileName = "eventList"
        self.eventList = []
        self.clientSocket = clientSocket
        self.getEvents()

    # Identify task for the exact function
    def work(self, task, event):
        processedObj = None
        if task == 'create':
            processedObj = self.createEvent(event)
        elif task == 'search':
            processedObj = self.searchEvent(event)
        elif task == 'updateEvent':
            self.update(event)
        return processedObj

    # Get all users to self.userList
    def getEvents(self):
        print("Loading events...")
        self.eventList = []
        try:
            file_object = open(self.eventListFileName, 'rb')
        except FileNotFoundError:
            file_object = open(self.eventListFileName, 'ab')
        try:
            while True:
                obj = pickle.load(file_object)
                self.eventList.append(obj)
        except EOFError:
            pass

    # Register new user
    def createEvent(self, event):
        for createdEvent in self.eventList:
            if event.title == createdEvent.title:
                print(event.title + " is not available")
                return event.title + " is not available"

        event = Event(event.title)
        fileObject = open(self.eventListFileName, 'ab')
        pickle.dump(event, fileObject)
        fileObject.close()
        self.eventList.append(event)
        print("Created Event:", event.title, "successfully")
        return True

    # Log in user
    def searchEvent(self, event):
        for createdEvent in self.eventList:
            if event.title == createdEvent.title:
                print("Event: ", event.title, "Event Found")
                return createdEvent
        print("Event: ", event.title, "Event Not Found")
        return "Event: ", event.title, "Event Not Found"

    #update user
    def update(self, event):
        for i in range(len(self.eventList)):
            if event.title == self.eventList[i].title:
                self.eventList[i] = event
        self.saveEvents()

    def saveEvents(self):
        fileObject = open(self.eventListFileName, 'wb')
        for createdEvent in self.eventList:
            pickle.dump(createdEvent, fileObject)
        fileObject.close()





