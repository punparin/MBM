class User:
    def __init__(self, username, password, email = ""):
        # system
        self.username = username
        self.password = password
        self.email = email

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

    def __str__(self):
        return self.username + " " + self.password + " " + self.email + " " + self.nickname + " " + self.address + " " + self.phone_number


