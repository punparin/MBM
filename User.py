class User:
    def __init__(self, username, password, email = None):
        self.username = username
        self.password = password
        self.email = email

    def __str__(self):
        return self.username + " " + self.password + " " + self.email


