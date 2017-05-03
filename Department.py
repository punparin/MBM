from anytree import Node, RenderTree
from Position import *

class InvalidArgument(Exception) : pass

class Department:
    def __init__(self, name):
        self.name = name
        self.positionTree = None

    def setName(self, name):
        self.name = name

    def addEmployee(self, position, employee):
        pos = self.searchPosition(position)
        if pos is None:
            raise InvalidArgument(position, "does not exist")
        else:
            pos = pos.name
            pos.insertUser(employee)

    def removeEmployee(self, employeeID):
        if self.positionTree is None:
            raise InvalidArgument(employeeID, "does not exist in", self.name)
        for pre, fill, node in RenderTree(self.positionTree):
            try:
                node.name.removeUser(employeeID)
                return
            except UserNotFound:
                 pass
        raise InvalidArgument(employeeID, "does not exist in", self.name)

    def findEmployeePosition(self, employeeID):
        if self.positionTree is None:
            return None
        for pre, fill, node in RenderTree(self.positionTree):
            if node.name.hasUser(employeeID):
                return node.name.name
        return None

    def searchPosition(self, position):
        if self.positionTree is None:
            return None
        for pre, fill, node in RenderTree(self.positionTree):
            if node.name.name == position:
                return node
        return None

    def addPosition(self, position, parent):
        pos = self.searchPosition(position)
        if pos is not None:
            raise InvalidArgument(position, "has already been created")
        elif self.positionTree is None:
            newPos = Position(position)
            self.positionTree = Node(newPos)
        elif parent is None:
            raise InvalidArgument("Root can be only one")
        else:
            par = self.searchPosition(parent)
            if par is None:
                raise InvalidArgument(parent, "does not exist")
            else:
                newPos = Position(position)
                Node(newPos, par)

    def removePosition(self, position):
        pos = self.searchPosition(position)
        if pos is None:
            raise InvalidArgument(position, "does not exist")
        if pos.parent is None:
            self.positionTree = None
        else:
            pos.parent = None

    def __str__(self):
        s = 'Deparment: ' + self.name
        if self.positionTree is not None:
            for pre, fill, node in RenderTree(self.positionTree):
                s += "\n\t%s%s" % (pre, node.name.show(pre))
        return s