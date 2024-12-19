# p2app/events/continents.py
#
# ICS 33 Spring 2024
# Project 2: Learning to Fly
#
# Events that are either related to searching for, creating, or editing continents
# in the database.
#
# See the project write-up for details on when these events are sent and by whom.
#
# YOU WILL NOT NEED TO MODIFY THIS FILE AT ALL

from collections import namedtuple



Continent = namedtuple('Continent', ['continent_id', 'continent_code', 'name'])

Continent.__annotations__ = {
    'continent_id': int | None,
    'continent_code': str | None,
    'name': str | None
}



class StartContinentSearchEvent:
    def __init__(self, continent_code: str, name: str):
        self._continent_code = continent_code
        self._name = name


    def continent_code(self) -> str:
        return self._continent_code


    def name(self) -> str:
        return self._name


    def __repr__(self) -> str:
        return f'{type(self).__name__}: continent_code = {repr(self._continent_code)}, name = {repr(self._name)}'



class ContinentSearchResultEvent:
    def __init__(self, continent: Continent):
        self._continent = continent


    def continent(self) -> Continent:
        return self._continent


    def __repr__(self) -> str:
        return f'{type(self).__name__}: continent = {repr(self._continent)}'



class LoadContinentEvent:
    def __init__(self, continent_id: int):
        self._continent_id = continent_id


    def continent_id(self) -> int:
        return self._continent_id


    def __repr__(self) -> str:
        return f'{type(self).__name__}: continent_id = {repr(self._continent_id)}'



class ContinentLoadedEvent:
    def __init__(self, continent: Continent):
        self._continent = continent


    def continent(self) -> Continent:
        return self._continent


    def __repr__(self) -> str:
        return f'{type(self).__name__}: continent = {repr(self._continent)}'



class SaveNewContinentEvent:
    def __init__(self, continent: Continent):
        self._continent = continent


    def continent(self) -> Continent:
        return self._continent


    def __repr__(self) -> str:
        return f'{type(self).__name__}: continent = {repr(self._continent)}'



class SaveContinentEvent:
    def __init__(self, continent: Continent):
        self._continent = continent


    def continent(self) -> Continent:
        return self._continent


    def __repr__(self) -> str:
        return f'{type(self).__name__}: continent = {repr(self._continent)}'



class ContinentSavedEvent:
    def __init__(self, continent: Continent):
        self._continent = continent


    def continent(self) -> Continent:
        return self._continent


    def __repr__(self) -> str:
        return f'{type(self).__name__}: continent = {repr(self._continent)}'



class SaveContinentFailedEvent:
    def __init__(self, reason: str):
        self._reason = reason


    def reason(self) -> str:
        return self._reason


    def __repr__(self) -> str:
        return f'{type(self).__name__}: reason = {repr(self._reason)}'
