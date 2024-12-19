# p2app/events/regions.py
#
# ICS 33 Spring 2024
# Project 2: Learning to Fly
#
# Events that are either related to searching for, creating, or editing regions
# in the database.
#
# See the project write-up for details on when these events are sent and by whom.
#
# YOU WILL NOT NEED TO MODIFY THIS FILE AT ALL

from collections import namedtuple



Region = namedtuple(
    'Region',
    ['region_id', 'region_code', 'local_code', 'name',
     'continent_id', 'country_id', 'wikipedia_link', 'keywords'])

Region.__annotations__ = {
    'region_id': int | None,
    'region_code': str | None,
    'local_code': str | None,
    'name': str | None,
    'continent_id': int | None,
    'country_id': int | None,
    'wikipedia_link': str | None,
    'keywords': str | None
}



class StartRegionSearchEvent:
    def __init__(self, region_code: str, local_code: str, name: str):
        self._region_code = region_code
        self._local_code = local_code
        self._name = name


    def region_code(self) -> str:
        return self._region_code


    def local_code(self) -> str:
        return self._local_code


    def name(self) -> str:
        return self._name


    def __repr__(self) -> str:
        return f'{type(self).__name__}: region_code = {repr(self._region_code)}, ' + \
               f'local_name = {repr(self._local_code)}, name = {repr(self._name)}'



class RegionSearchResultEvent:
    def __init__(self, region: Region):
        self._region = region


    def region(self) -> Region:
        return self._region


    def __repr__(self) -> str:
        return f'{type(self).__name__}: region = {repr(self._region)}'



class LoadRegionEvent:
    def __init__(self, region_id: int):
        self._region_id = region_id


    def region_id(self) -> int:
        return self._region_id


    def __repr__(self) -> str:
        return f'{type(self).__name__}: region_id = {repr(self._region_id)}'



class RegionLoadedEvent:
    def __init__(self, region: Region):
        self._region = region


    def region(self) -> Region:
        return self._region


    def __repr__(self) -> str:
        return f'{type(self).__name__}: region = {repr(self._region)}'



class SaveNewRegionEvent:
    def __init__(self, region: Region):
        self._region = region


    def region(self) -> Region:
        return self._region


    def __repr__(self) -> str:
        return f'{type(self).__name__}: region = {repr(self._region)}'



class SaveRegionEvent:
    def __init__(self, region: Region):
        self._region = region


    def region(self) -> Region:
        return self._region


    def __repr__(self) -> str:
        return f'{type(self).__name__}: region = {repr(self._region)}'



class RegionSavedEvent:
    def __init__(self, region: Region):
        self._region = region


    def region(self) -> Region:
        return self._region


    def __repr__(self) -> str:
        return f'{type(self).__name__}: region = {repr(self._region)}'



class SaveRegionFailedEvent:
    def __init__(self, reason: str):
        self._reason = reason


    def reason(self) -> str:
        return self._reason


    def __repr__(self) -> str:
        return f'{type(self).__name__}: reason = {repr(self._reason)}'
