from anytree import Node, RenderTree
from Position import *

class InvalidArgument(Exception) : pass

class Department:
    def __init__(self, name):
        self.name = name
        self.positionTree = None

    def setName(self, name):
        self.name = name

    def addEmployee(self, position, user):
        pos = self.searchPosition(position)
        if pos is None:
            raise InvalidArgument(position, "does not exist")
        else:
            pos = pos.name
            pos.insertUser(user)

    def removeEmployee(self, employee):
        for pre, fill, node in RenderTree(self.positionTree):
            try:
                node.name.removeUser(employee)
                return
            except UserNotFound:
                 pass
        raise InvalidArgument(employee, "does not exist in", self.name)

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
        pos.parent = None

    def __str__(self):
        s = 'Deparment: ' + self.name
        if self.positionTree is not None:
            for pre, fill, node in RenderTree(self.positionTree):
                s += "\n\t%s%s" % (pre, node.name.show(pre))
        return s