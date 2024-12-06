class TakenException(Exception):
    def __init__(self, message='Exception: Input taken'):
        self.message = message
