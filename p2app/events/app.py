class ErrorEvent:
    def __init__(self, message: str):
        self._message = message


    def message(self) -> str:
        return self._message


    def __repr__(self) -> str:
        return f'{type(self).__name__}: message = {repr(self._message)}'



class QuitInitiatedEvent:
    def __repr__(self) -> str:
        return f'{type(self).__name__}'



class EndApplicationEvent:
    def __repr__(self) -> str:
        return f'{type(self).__name__}'
