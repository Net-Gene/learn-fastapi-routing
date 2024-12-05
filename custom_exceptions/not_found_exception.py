class NotFoundException(Exception):
    def __init__(self, message='Exception: Item not found'):
        self.message = message
