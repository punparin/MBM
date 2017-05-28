import pickle
import io
from Project import *

class ProjectManager:
    def __init__(self):
        self.projectListFileName = "projectList"
        self.projectList = {}
        self.getProjects()

    # Identify task for the exact function
    def work(self, task, obj):
        processedObj = None
        if task == 'create':
            processedObj = self.createProject(obj)
        elif task == 'search':
            processedObj = self.searchProject(obj)
        elif task == 'updateProject':
            self.update(obj)
        return processedObj

    # Get all users to self.userList
    def getProjects(self):
        print("Loading projects...")
        self.projectList = []
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

    # Update project
    def update(self, project):
        for i in range(len(self.projectList)):
            if project.title == self.projectList[i].title:
                self.projectList[i] = project
        self.saveProjects()

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