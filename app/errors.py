class ServerException(Exception):
    name: str
    text: str

    def __init__(self, name: str, error: str):
        self.name = name
        self.text = error

    def __str__(self):
        return str(vars(self))
