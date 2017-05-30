import pickle
import io
import time
import copy
from Department import *

class DepartmentManager:
    def __init__(self, userManager):
        self.departmentFileName = 'departmentList'
        self.userManager = userManager
        self.departmentList = []
        self.getDepartments()

    # Identify task for the exact function
    def work(self, task, obj = None):
        processedObj = None
        if task == 'getInitialInfo':
            processedObj = self.getInitialInfo()
        elif task == 'addDepartment':
            processedObj = self.addDepartment(obj)
        elif task == 'removeDepartment':
            processedObj = self.removeDepartment(obj)
        elif task == 'addEmployee':
            dep, pos, username = obj
            processedObj = self.addEmployee(dep, pos, username)
        elif task == 'removeEmployee':
            dep, username = obj
            processedObj = self.removeEmployee(dep, username)
        elif task == 'addPosition':
            if len(obj) == 2:
                processedObj = self.addPosition(obj[0], obj[1])
            else:
                processedObj = self.addPosition(obj[0], obj[1], obj[2])
        elif task == 'removePosition':
            dep, pos = obj
            processedObj = self.removePosition(dep, pos)
        return processedObj

    def searchDepartment(self, department):
        for dep in self.departmentList:
            if dep.name == department:
                return dep
        return None

    def addPosition(self, department, position, parent = None):
        dep = self.searchDepartment(department)
        if dep is None:
            return department + ' does not exist'
        try:
            dep.addPosition(position, parent)
            self.saveDepartments()
            self.notifyAll()
            return "Added " + position + " successfully"
        except InvalidArgument as err:
            return position + " does not exist"

    # notify All to getInitialInfo
    def notifyAll(self):
        for username in self.userManager.clientSocketList:
            try:
                clientSocket = self.userManager.clientSocketList[username]
                clientSocket.send('getInitialInfo'.encode('ascii'))
                obj = pickle.dumps(self.getInitialInfo())
                clientSocket.send(obj)
            except KeyError:
                pass
        time.sleep(0.5)

    def getInitialInfo(self):
        initialInfo = copy.deepcopy(self.departmentList)
        for department in initialInfo:
            if department.positionTree is not None:
                for pre, fill, node in RenderTree(department.positionTree):
                    newEmployeeList = {}
                    for id in node.name.employeeList:
                        username = node.name.employeeList[id]
                        user = self.userManager.findByUsername(username)
                        newEmployeeList[id] = user.dummy()
                    node.name.employeeList = newEmployeeList
        return initialInfo

    def removePosition(self, department, position):
        dep = self.searchDepartment(department)
        if dep is None:
            return department + ' does not exist'
        try:
            dep.removePosition(position)
            self.saveDepartments()
            self.notifyAll()
            return "Removed " + position + " successfully"
        except InvalidArgument as err:
            return position + " does not exist"

    def searchPosition(self, department, position):
        dep = self.searchDepartment(department)
        if dep is None:
            print(department, 'does not exist')
            return
        else:
            return dep.searchPosition(position)

    def getDepartments(self):
        print("Loading departments...")
        try:
            fileObject = open(self.departmentFileName, 'rb')
        except FileNotFoundError:
            fileObject = open(self.departmentFileName, 'ab')
        try:
            while True:
                obj = pickle.load(fileObject)
                self.departmentList.append(obj)
        except EOFError:
            fileObject.close()
        except (AttributeError, io.UnsupportedOperation):
            fileObject.close()

    def saveDepartment(self, department):
        fileObject = open(self.departmentFileName, 'ab')
        pickle.dump(department, fileObject)
        fileObject.close()

    def saveDepartments(self):
        fileObject = open(self.departmentFileName, 'wb')
        for department in self.departmentList:
            pickle.dump(department, fileObject)
        fileObject.close()

    def removeDepartment(self, department):
        dep = self.searchDepartment(department)
        if dep is None:
            return department + ' does not exist'
        else:
            self.departmentList.remove(dep)
            self.saveDepartments()
            self.notifyAll()
            return 'Removed ' + department + ' successfully'

    def addDepartment(self, department):
        dep = self.searchDepartment(department)
        if dep is not None:
            return department + ' already exists'
        dep = Department(department)
        self.departmentList.append(dep)
        self.saveDepartment(dep)
        # notify All to getInitialInfo
        self.notifyAll()
        return 'Created ' + department + ' successfully'

    def addEmployee(self, department, position, username):
        dep = self.searchDepartment(department)
        if dep is not None:
            user = self.userManager.findByUsername(username)
            if user is not None:
                try:
                    dep.addEmployee(position, user)
                    user.position[department] = position
                    self.userManager.saveUsers()
                    self.saveDepartments()
                    # notify All to getInitialInfo
                    self.notifyAll()
                    return 'Added ' + username + ' to ' + department + ' successfully'
                except InvalidArgument:
                    return position + ' does not exist'
            else:
                return username + ' does not exist'
        else:
            return department + ' does not exist'

    def removeEmployee(self, department, username):
        dep = self.searchDepartment(department)
        if dep is not None:
            user = self.userManager.findByUsername(username)
            if user is not None:
                dep.removeEmployee(user.id)
                user.position = ""
                self.userManager.saveUsers()
                self.saveDepartments()
                # notify All to getInitialInfo
                self.notifyAll()
                return 'Removed ' + username + ' from ' + department + ' successfully'
            else:
                return username + ' does not exist'
        else:
            return department + ' does not exist'

    def findEmployeePosition(self, department, username):
        dep = self.searchDepartment(department)
        s = ""
        if dep is not None:
            user = self.userManager.findByUsername(username)
            if user is not None:
                pos = dep.findEmployeePosition(user.id)
                if pos is not None:
                    print(pos + ": " + username + " found")
                    return True
                else:
                    print(username, 'does not exist in', department)
                    return False
            else:
                print(username, 'does not exist')
                return False
        else:
            print(department, 'does not exist')
            return False

    def removeDepartmentList(self):
        fileObject = open(self.departmentFileName, 'wb')
        fileObject.close()
        self.departmentList = []
        print('Cleared successfully')
        # notify All to getInitialInfo
        self.notifyAll()

    def getUserPermission(self, username):
        user = self.userManager.findByUsername(username)
        permission = copy.deepcopy(user.position)
        for dep in permission:
            pos = self.searchPosition(dep, permission[dep])
            permission[dep] = pos.getPerMissions()
        return permission

    def showDepartment(self, department):
        dep = self.searchDepartment(department)
        if dep is not None:
            print(dep)
        else:
            print(department, 'does not exist')

    def showDepartmentList(self):
        for department in self.departmentList:
            print('\n-', department)