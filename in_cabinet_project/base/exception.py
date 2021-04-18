class ViewException(Exception):
    def __init__(self, message: str = "", **kwds: object) -> None:
        self.message = message