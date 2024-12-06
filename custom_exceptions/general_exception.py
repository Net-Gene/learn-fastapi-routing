class GeneralException(Exception):
    def __init__(self, message='Exception: Internal Server Error'):
        super(GeneralException, self).__init__(message)
        self.message = message
