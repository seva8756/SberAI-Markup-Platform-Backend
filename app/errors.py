class ServerException(Exception):
    name: str
    message: str

    def __init__(self, name: str, message: str):
        self.name = name
        self.message = message

    def __str__(self):
        return str(vars(self))
