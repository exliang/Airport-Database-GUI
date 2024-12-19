# p2app/events/database.py
#
# ICS 33 Spring 2024
# Project 2: Learning to Fly
#
# Events related to the opening and closing of the database.
#
# See the project write-up for details on when these events are sent and by whom.
#
# YOU WILL NOT NEED TO MODIFY THIS FILE AT ALL

from pathlib import Path



class OpenDatabaseEvent:
    def __init__(self, path: Path):
        self._path = path


    def path(self) -> Path:
        return self._path


    def __repr__(self) -> str:
        return f'{type(self).__name__}: path = {repr(self._path)}'



class CloseDatabaseEvent:
    def __repr__(self) -> str:
        return f'{type(self).__name__}'



class DatabaseOpenedEvent:
    def __init__(self, path: Path):
        self._path = path


    def path(self) -> Path:
        return self._path


    def __repr__(self) -> str:
        return f'{type(self).__name__}: path = {repr(self._path)}'



class DatabaseOpenFailedEvent:
    def __init__(self, reason: str):
        self._reason = reason


    def reason(self) -> str:
        return self._reason


    def __repr__(self) -> str:
        return f'{type(self).__name__}: reason = {repr(self._reason)}'



class DatabaseClosedEvent:
    def __repr__(self) -> str:
        return f'{type(self).__name__}'
