# An object that represents the engine of the application.

from .continent_events import *
from .country_events import *
from .region_events import *

class Engine:
    """An object that represents the application's engine, whose main role is to
    process events sent to it by the user interface, then generate events that are
    sent back to the user interface in response, allowing the user interface to be
    unaware of any details of how the engine is implemented.
    """

    def __init__(self):
        """Initializes the engine"""
        self.connection = ""


    def process_event(self, event):
        """A generator function that processes one event sent from the user interface,
        yielding zero or more events in response."""

        # Application-level events
        if isinstance(event, OpenDatabaseEvent):
            try:
                self.connection = sqlite3.connect(event.path().name)
                self.connection.execute("PRAGMA foreign_keys = ON;")
            except Exception as e:
                yield DatabaseOpenFailedEvent(f'Error: {e}')
            else:
                if not valid_database_file(event.path().name):
                    yield DatabaseOpenFailedEvent('Database is an invalid db file or is not even a db file type.')
                elif not tables_exist_in_dbfile(event.path().name):
                    yield DatabaseOpenFailedEvent("Database doesn't contain the necessary tables")
                else:
                    yield DatabaseOpenedEvent(Path(event.path()))
        if isinstance(event, QuitInitiatedEvent):
            try:
                yield EndApplicationEvent()
            except Exception as e:
                yield ErrorEvent(f"Error: {e}")
        if isinstance(event, CloseDatabaseEvent):
            try:
                self.connection.close()
                yield DatabaseClosedEvent()
            except Exception as e:
                yield ErrorEvent(f"Error: {e}")

        # Continent-related events
        if isinstance(event, StartContinentSearchEvent):
            for result in start_continent_search(self.connection, event):
                yield result
        if isinstance(event, LoadContinentEvent):
            for result in load_continent(self.connection, event):
                yield result
        if isinstance(event, SaveNewContinentEvent):
            for result in save_new_continent(self.connection, event):
                yield result
        if isinstance(event, SaveContinentEvent):
            for result in save_continent(self.connection, event):
                yield result

        # Country-related events
        if isinstance(event, StartCountrySearchEvent):
            for result in start_country_search(self.connection, event):
                yield result
        if isinstance(event, LoadCountryEvent):
            for result in load_country(self.connection, event):
                yield result
        if isinstance(event, SaveNewCountryEvent):
            for result in save_new_country(self.connection, event):
                yield result
        if isinstance(event, SaveCountryEvent):
            for result in save_country(self.connection, event):
                yield result

        # Region-related events
        if isinstance(event, StartRegionSearchEvent):
            for result in start_region_search(self.connection, event):
                yield result
        if isinstance(event, LoadRegionEvent):
            for result in load_region(self.connection, event):
                yield result
        if isinstance(event, SaveNewRegionEvent):
            for result in save_new_region(self.connection, event):
                yield result
        if isinstance(event, SaveRegionEvent):
            for result in save_region(self.connection, event):
                yield result
