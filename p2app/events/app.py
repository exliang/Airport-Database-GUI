# p2app/events/app.py
#
# ICS 33 Spring 2024
# Project 2: Learning to Fly
#
# Application-level events that are either sent by the user interface to the
# engine, or from the engine back to the user interface.
#
# See the project write-up for details on when these events are sent and by whom.
#
# YOU WILL NOT NEED TO MODIFY THIS FILE AT ALL



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
