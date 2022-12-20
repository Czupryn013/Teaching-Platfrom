from enum import Enum


class User:
    def __init__(self, id, username, password="-"):
        self.id = id
        self.username = username
        self.password = password

class CensuredUser:
    def __init__(self, id, username):
        self.id = id
        self.username = username

class Role(Enum):
    STUDENT = 0
    TEACHER = 1
    ADMIN = 2