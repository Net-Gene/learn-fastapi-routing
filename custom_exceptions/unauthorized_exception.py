class UnauthorizedException(Exception):
    def __init__(self, message='Exception: Login is required'):
        super(UnauthorizedException, self).__init__(message)
        self.message = message
