import pickle
from Project import *

class ProjectManager:
    def __init__(self, clientSocket):
        self.projectListFileName = "projectList"
        self.projectList = []
        self.clientSocket = clientSocket
        self.getProjects()

    # Identify task for the exact function
    def work(self, task, project):
        processedObj = None
        if task == 'create':
            processedObj = self.createProject(project)
        elif task == 'search':
            processedObj = self.searchProject(project)
        elif task == 'updateProject':
            self.update(project)
        return processedObj

    # Get all users to self.userList
    def getProjects(self):
        print("Loading projects...")
        self.projectList = []
        try:
            file_object = open(self.projectListFileName, 'rb')
        except FileNotFoundError:
            file_object = open(self.projectListFileName, 'ab')
        try:
            while True:
                obj = pickle.load(file_object)
                self.projectList.append(obj)
        except EOFError:
            pass

    # Register new user
    def createProject(self, project):
        for createdProject in self.projectList:
            if project.title == createdProject.title:
                print(project.title + " is not available")
                return project.title + " is not available"

        project = Project(project.title)
        fileObject = open(self.projectListFileName, 'ab')
        pickle.dump(project, fileObject)
        fileObject.close()
        self.projectList.append(project)
        print("Created Event:", project.title, "successfully")
        return True

    # Log in user
    def searchProject(self, project):
        for createdProject in self.projectList:
            if project.title == createdProject.title:
                print("Project: ", project.title, "Project Found")
                return createdProject
        print("Project: ", project.title, "Project Not Found")
        return "Project: ", project.title, "Project Not Found"

    #update user
    def update(self, project):
        for i in range(len(self.projectList)):
            if project.title == self.projectList[i].title:
                self.projectList[i] = project
        self.saveProjects()

    def saveProjects(self):
        fileObject = open(self.projectListFileName, 'wb')
        for createdProject in self.projectList:
            pickle.dump(createdProject, fileObject)
        fileObject.close()





