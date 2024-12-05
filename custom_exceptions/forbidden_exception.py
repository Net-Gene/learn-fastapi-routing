class ForbiddenException(Exception):
    def __init__(self, message='Exception: Forbidden'):
        super(ForbiddenException, self).__init__(message)
        self.message = message
