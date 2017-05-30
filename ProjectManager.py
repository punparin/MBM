import pickle
import io
import time
import copy
from Project import *

class ProjectManager:
    def __init__(self, userManager, departmentManager):
        self.projectListFileName = "projectList"
        self.userManager = userManager
        self.departmentManager = departmentManager
        self.projectList = {}
        self.getProjects()

    # Identify task for the exact function
    def work(self, task, obj):
        processedObj = None
        if task == 'createProject':
            processedObj = self.createProject(obj)
        elif task == 'searchProject':
            processedObj = self.searchProject(obj)
        elif task == 'updateProject':
            self.update(obj)
        elif task == 'removeProject':
            self.removeProject(obj)
        elif task == 'getInitialProject':
            processedObj = self.getInitialProject()
        return processedObj

    def getInitialProject(self):
        return self.projectList

    # Get all users to self.userList
    def getProjects(self):
        print("Loading projects...")
        self.projectList = {}
        try:
            fileObject = open(self.projectListFileName, 'rb')
        except FileNotFoundError:
            fileObject = open(self.projectListFileName, 'ab')
        try:
            while True:
                obj = pickle.load(fileObject)
                self.projectList[obj.title] = obj
        except EOFError:
            fileObject.close()
        except (AttributeError, io.UnsupportedOperation):
            fileObject.close()

    # Create a new project
    def createProject(self, project):
        for title in self.projectList:
            if project.title == self.projectList[title].title:
                return False
        fileObject = open(self.projectListFileName, 'ab')
        pickle.dump(project, fileObject)
        fileObject.close()
        self.projectList[project.title] = project
        self.saveProject(project)
        self.notifyAll()
        return True

    # Remove a project
    def removeProject(self, projectTitle):
        try:
            del self.projectList[projectTitle]
            self.saveProjects()
            self.notifyAll()
        except KeyError:
            return 'not found'

    # Find a project by its title
    def findByTitle(self, title):
        try:
            return self.projectList[title]
        except KeyError:
            return None

    # Search for a project
    def searchProject(self, projectTitle):
        project = self.findByTitle(projectTitle)
        if project is not None:
            print("Project: ", project.title, "Project Found")
            return project
        else:
            print("Project: ", project.title, "Project Not Found")
            return None

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

    # notify All to getInitialProject
    def notifyAll(self, project = None):
        for username in self.userManager.clientSocketList:
            try:
                clientSocket = self.userManager.clientSocketList[username]
                if project is None:
                    obj = pickle.dumps(['getInitialProject', self.getInitialProject()])
                else:
                    obj = pickle.dumps(['updateProject', project])
                clientSocket.send(obj)
            except KeyError:
                pass
        time.sleep(0.5)

    # Update project
    def update(self, project):
        for title in self.projectList:
            if project.title == self.projectList[title].title:
                self.projectList[title] = project
        self.saveProjects()
        # notify all to getInitialProject
        self.notifyAll(project)

    # Save project
    def saveProject(self, project):
        fileObject = open(self.projectListFileName, 'ab')
        pickle.dump(project, fileObject)
        fileObject.close()

    # Save all projects
    def saveProjects(self):
        fileObject = open(self.projectListFileName, 'wb')
        for title in self.projectList:
            pickle.dump(self.projectList[title], fileObject)
        fileObject.close()