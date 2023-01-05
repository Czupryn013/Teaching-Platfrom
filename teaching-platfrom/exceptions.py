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

class PasswordToWeakError(Exception):
    def __init__(self, message="Given password is to weak."):
        self.message = message
        self.status = 406
        logging.warning(message)

    def __str__(self):
        return f"Error: {self.message} Status: {self.status}"

class IncorrectUsername(Exception):
    def __init__(self):
        self.message = "Incorrect username."
        self.status = 406
        logging.warning(self.message)

    def __str__(self):
        return f"Error: {self.message} Status: {self.status}"









