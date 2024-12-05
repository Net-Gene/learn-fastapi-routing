class UsernameTakenException(Exception):
    def __init__(self, message='Exception: Username taken'):
        self.message = message
