class User:
    def __init__(self):
        self.username = None
        self.password = None
        self.email = None

    def register(self, username, password, email):
        isValid = True
        self.username = username
        self.password = password
        self.email = email
        return isValid

    def __str__(self):
        return self.username + " " + self.password + " " + self.email


