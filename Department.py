from anytree import Node, RenderTree
from Position import *

class InvalidArgument(Exception) : pass

class Department:
    departments = []
    def __init__(self, name):
        if name in self.departments:
            raise InvalidArgument('The name has already been used')
        self.name = name
        self.positionTree = None

    def setName(self, name):
        if name in self.departments:
            raise InvalidArgument('The name has already been used')
        self.name = name

    def addEmployee(self, position, user):
        pos = self.searchPosition(position)
        if pos is None:
            raise InvalidArgument(position, "does not exist")
        else:
            pos = pos.name
            pos.insertUser(user)

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
            return True
        else:
            par = self.searchPosition(parent)
            if par is None:
                raise InvalidArgument(parent, "does not exist")
            else:
                newPos = Position(position)
                Node(newPos, par)
                return True

    def removePosition(self, position):
        pass

    def __str__(self):
        s = 'Deparment: ' + self.name
        if self.positionTree is not None:
            for pre, fill, node in RenderTree(self.positionTree):
                s += "\n\t%s%s" % (pre, node.name.show(pre))
        return s