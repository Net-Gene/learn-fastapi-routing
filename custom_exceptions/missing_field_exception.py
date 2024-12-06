class MissingFieldException(Exception):
    def __init__(self, message='Exception: Missing a field'):
        super(MissingFieldException, self).__init__(message)
        self.message = message
