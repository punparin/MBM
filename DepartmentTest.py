import unittest
import random
from User import *
from Department import *

class DepartmentTest(unittest.TestCase):
    def setUp(self):
        self.department = Department('Test')

    def test_searchPosition(self):
        # find empty positionTree
        self.assertEqual(None, self.department.searchPosition('Test'))
        # found
        self.department.addPosition('Test', None)
        self.assertEqual(str(RenderTree(Node(Position('Test')))),
                         str(RenderTree(self.department.searchPosition('Test'))))
        # not found
        self.assertEqual(None, self.department.searchPosition('A'))

    def test_addPosition(self):
        self.assertEqual(None, self.department.positionTree)
        # add a root node
        self.department.addPosition('A', None)
        self.assertNotEqual(None, self.department.positionTree)
        # root can be only one
        self.assertRaises(InvalidArgument, self.department.addPosition, 'B', None)
        # add a child node
        temp = Node(Position('A'))
        Node(Position('B'), temp)
        renderTemp = str(RenderTree(temp))
        self.department.addPosition('B', 'A')
        renderTree = str(RenderTree(self.department.positionTree))
        self.assertEqual(renderTemp, renderTree)
        # already exists
        self.assertRaises(InvalidArgument, self.department.addPosition, 'B', 'A')
        # parent does not exist
        self.assertRaises(InvalidArgument, self.department.addPosition, 'B', 'C')

    def test_removePosition(self):
        self.assertEqual(None, self.department.positionTree)
        # remove non-existent node
        self.assertRaises(InvalidArgument, self.department.removePosition, 'A')
        # add A-B into positionTree
        self.department.addPosition('A', None)
        self.department.addPosition('B', 'A')
        # remove a child node
        temp = Node(Position('A'))
        renderTemp = str(RenderTree(temp))
        self.department.removePosition('B')
        renderTree = str(RenderTree(self.department.positionTree))
        self.assertEqual(renderTemp, renderTree)
        # remove a root node
        self.department.removePosition('A')
        self.assertEqual(None, self.department.positionTree)

    def test_positionSanity(self):
        self.department.addPosition('A', None)
        posList = ['A']
        # add A-Z into positionTree
        for i in range(ord('B'), ord('Z') + 1):
            self.department.addPosition(chr(i), random.choice(posList))
            posList.append(chr(i))
        self.assertNotEqual(None, self.department.positionTree) # not equal to None
        # remove A-Z from positionTree
        for i in range(ord('Z'), ord('A') - 1, -1):
            self.department.removePosition(chr(i))
        self.assertEqual(None, self.department.positionTree) # equal to None

    def test_findEmployeePosition(self):
        # find in empty positionTree
        user = User('TestA')
        user.id = 1
        self.assertEqual(None, self.department.findEmployeePosition(user.id))
        # find non-existent employee in non-empty positionTree
        self.department.addPosition('A', None)
        self.assertEqual(None, self.department.findEmployeePosition(user.id))
        # find existent employee
        self.department.addEmployee('A', user)
        self.assertEqual('A', self.department.findEmployeePosition(user.id))

    def test_addEmployee(self):
        user = User('TestA')
        user.id = 1
        # add employee in an non-existent position
        self.assertRaises(InvalidArgument, self.department.addEmployee, 'A', user)
        # add employee
        self.department.addPosition('A', None)
        self.department.addEmployee('A', user)
        self.assertEqual('A', self.department.findEmployeePosition(user.id))

    def test_removeEmployee(self):
        user = User('TestA')
        user.id = 1
        user2 = User('TestB')
        user2.id = 2
        # remove in an empty positionTree
        self.assertRaises(InvalidArgument, self.department.removeEmployee, user.id)
        # employee not found
        self.department.addPosition('A', None)
        self.department.addEmployee('A', user)
        self.assertRaises(InvalidArgument, self.department.removeEmployee, user2.id)
        # employee found
        self.department.removeEmployee(user.id)
        self.assertEqual(None, self.department.findEmployeePosition(user.id))

    def test_employeeSanity(self):
        # add A-E into PositionTree
        self.department.addPosition('A', None)
        posList = ['A']
        count = 1
        for i in range(ord('B'), ord('E') + 1):
            self.department.addPosition(chr(i), random.choice(posList))
            posList.append(chr(i))
            # add 10 employees into each position
            for j in range(count, count + 10):
                # non-existent user
                user = User(str(j))
                user.id = j
                self.assertEqual(None, self.department.findEmployeePosition(user.id))
                self.department.addEmployee(chr(i), user)
            count += 10
        # find existent employees
        for i in range(1, count):
            self.assertNotEqual(None, self.department.findEmployeePosition(i))
        # remove employees
        for i in range(1, count):
            self.department.removeEmployee(i)
        # find non-existent users
        for i in range(1, count):
            self.assertEqual(None, self.department.findEmployeePosition(i))

if __name__ == '__main__':
    unittest.main()
