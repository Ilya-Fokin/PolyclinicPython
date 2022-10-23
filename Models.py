from werkzeug.security import generate_password_hash, check_password_hash


class User:
    def __init__(self, id, login, password, role):
        self.id = id
        self.login = login
        self.password = password
        self.role = role


class Role:
    def __init__(self, role):
        self.id = id
        self.role = role
