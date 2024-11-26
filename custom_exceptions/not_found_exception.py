class NotFoundexception(Exception):
    def __init__(self, message='item not found'):
        self.message = message