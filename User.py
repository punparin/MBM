class User:
    def __init__(self, username, password = "", email = ""):
        # system
        self.username = username
        self.password = password
        self.email = email
        self.id = ""

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
        self.isActivated = True

    def __str__(self):
        return 'User: ' + format(self.id, '05d') + " " + self.username + " " + self.email


