# p2app/events/countries.py
#
# ICS 33 Spring 2024
# Project 2: Learning to Fly
#
# Events that are either related to searching for, creating, or editing countries
# in the database.
#
# See the project write-up for details on when these events are sent and by whom.
#
# YOU WILL NOT NEED TO MODIFY THIS FILE AT ALL

from collections import namedtuple



Country = namedtuple(
    'Country',
    ['country_id', 'country_code', 'name', 'continent_id', 'wikipedia_link', 'keywords'])

Country.__annotations__ = {
    'country_id': int | None,
    'country_code': str | None,
    'name': str | None,
    'continent_id': int | None,
    'wikipedia_link': str | None,
    'keywords': str | None
}



class StartCountrySearchEvent:
    def __init__(self, country_code: str, name: str):
        self._country_code = country_code
        self._name = name


    def country_code(self) -> str:
        return self._country_code


    def name(self) -> str:
        return self._name


    def __repr__(self) -> str:
        return f'{type(self).__name__}: country_code = {repr(self._country_code)}, name = {repr(self._name)}'



class CountrySearchResultEvent:
    def __init__(self, country: Country):
        self._country = country


    def country(self) -> Country:
        return self._country


    def __repr__(self) -> str:
        return f'{type(self).__name__}: country = {repr(self._country)}'



class LoadCountryEvent:
    def __init__(self, country_id: int):
        self._country_id = country_id


    def country_id(self) -> int:
        return self._country_id


    def __repr__(self) -> str:
        return f'{type(self).__name__}: country_id = {repr(self._country_id)}'



class CountryLoadedEvent:
    def __init__(self, country: Country):
        self._country = country


    def country(self) -> Country:
        return self._country


    def __repr__(self) -> str:
        return f'{type(self).__name__}: country = {repr(self._country)}'



class SaveNewCountryEvent:
    def __init__(self, country: Country):
        self._country = country


    def country(self) -> Country:
        return self._country


    def __repr__(self) -> str:
        return f'{type(self).__name__}: country = {repr(self._country)}'



class SaveCountryEvent:
    def __init__(self, country: Country):
        self._country = country


    def country(self) -> Country:
        return self._country


    def __repr__(self) -> str:
        return f'{type(self).__name__}: country = {repr(self._country)}'



class CountrySavedEvent:
    def __init__(self, country: Country):
        self._country = country


    def country(self) -> Country:
        return self._country


    def __repr__(self) -> str:
        return f'{type(self).__name__}: country = {repr(self._country)}'



class SaveCountryFailedEvent:
    def __init__(self, reason: str):
        self._reason = reason


    def reason(self) -> str:
        return self._reason


    def __repr__(self) -> str:
        return f'{type(self).__name__}: reason = {repr(self._reason)}'
