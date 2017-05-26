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
        self.position = ""
        self.department = ""
        self.biology = ""
        self.nationality =""

        self.isAdmin = False
        self.status = "Offline"

    def dummy(self):
        user = User(self.username)

        user.username = self.username
        user.email = self.email
        user.id = self.id

        user.name = self.name
        user.middle_name = self.middle_name
        user.last_name = self.last_name
        user.nickname = self.nickname
        user.address = self.address
        user.phone_number = self.phone_number
        user.birth_date = self.birth_date
        user.position = self.position
        user.department = self.department
        user.biology = self.biology
        user.nationality = self.nationality

        user.isAdmin = self.isAdmin
        user.status = self.status

        return user

    def __str__(self):
        if self.id is None:
            return 'User: ' + self.username + " " + self.email
        return 'User: ' + format(self.id, '05d') + " " + self.username + " " + self.email