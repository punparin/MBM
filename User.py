import copy

class User:
    def __init__(self, username, password = "", email = ""):
        # system
        self.username = username
        self.password = password
        self.email = email
        self.id = None

        #user
        self.name = ""
        self.middle_name = ""
        self.last_name = ""
        self.nickname = ""
        self.address = ""
        self.phone_number = ""
        self.birth_date = ""
        self.position = []
        self.department = ""
        self.biology = ""
        self.nationality =""

        self.isAdmin = False
        self.status = "Offline"

    def deepcopy(self):
        user = copy.copy(self)
        user.password = ""
        return user

    def dummy(self):
        user = User(self.username)
        user.id = self.id
        user.name = self.name
        user.last_name = self.lastname
        user.status = self.status

    def __str__(self):
        if self.id is None:
            return 'User: ' + self.username + " " + self.email
        return 'User: ' + format(self.id, '05d') + " " + self.username + " " + self.email + str(self.position)