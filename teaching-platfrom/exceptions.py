import logging


class UserDosentExistError(Exception):
    def __init__(self):
        self.message = "User with this id dosen't exist."
        self.status = 404
        logging.warning("User with this id dosen't exist.")

    def __str__(self):
        return f"Error: {self.message} Status: {self.status}"

class UsernameTakenError(Exception):
    def __init__(self):
        self.message = "Username alreday taken, pick a diffrent one."
        self.status = 409
        logging.warning("Username alreday taken, pick a diffrent one.")

    def __str__(self):
        return f"Error: {self.message} Status: {self.status}"