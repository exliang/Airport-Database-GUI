# p2app/views/main.py
#
# ICS 33 Spring 2024
# Project 2: Learning to Fly
#
# The outermost shell of the user interface.
#
# YOU WILL NOT NEED TO MODIFY THIS FILE AT ALL

import tkinter
import tkinter.messagebox
from p2app.events import *
from .continents import ContinentsView
from .countries import CountriesView
from .empty import EmptyView
from .events import *
from .event_handling import EventHandler
from .menus import MainMenu
from .regions import RegionsView



_INITIAL_WINDOW_WIDTH = 800
_INITIAL_WINDOW_HEIGHT = 600
_PROJECT_NAME = 'ICS 33 - Project 2'
_MISSING_DATABASE_NAME = '[no database open]'



class MainView(tkinter.Tk, EventHandler):
    def __init__(self, event_bus):
        super().__init__()
        self.geometry(f'{_INITIAL_WINDOW_WIDTH}x{_INITIAL_WINDOW_HEIGHT}')
        self.config(menu = MainMenu(self))
        self._event_bus = event_bus
        self._current_view = None
        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)


    def initiate_event(self, event):
        if is_internal_event(event):
            self.handle_event(event)
        else:
            self._event_bus.initiate_event(event)


    def run(self):
        self._switch_view(EmptyView(self))
        self._update_database_path(None)
        self.mainloop()


    def on_event(self, event):
        if isinstance(event, ShowEditContinentsViewEvent):
            self._switch_view(ContinentsView(self))
        elif isinstance(event, ShowEditCountriesViewEvent):
            self._switch_view(CountriesView(self))
        elif isinstance(event, ShowEditRegionsViewEvent):
            self._switch_view(RegionsView(self))
        elif isinstance(event, DatabaseOpenedEvent):
            self._update_database_path(event.path())
        elif isinstance(event, DatabaseClosedEvent):
            self._update_database_path(None)
            self._switch_view(EmptyView(self))
        elif isinstance(event, DatabaseOpenFailedEvent):
            self._update_database_path(None)
            self._switch_view(EmptyView(self))
            tkinter.messagebox.showerror('Could Not Open Database', event.reason())
        elif isinstance(event, EnableDebugModeEvent):
            self._event_bus.enable_debug_mode()
        elif isinstance(event, DisableDebugModeEvent):
            self._event_bus.disable_debug_mode()


    def on_event_post(self, event):
        if isinstance(event, EndApplicationEvent):
            self.destroy()
        elif isinstance(event, ErrorEvent):
            tkinter.messagebox.showerror('Error', event.message())


    def _switch_view(self, view):
        if self._current_view:
            self._current_view.destroy()

        self._current_view = view
        self._current_view.grid(row = 0, column = 0, sticky = tkinter.NSEW, padx = 5, pady = 5)


    def _update_database_path(self, path):
        if path:
            visible_name = path.name
        else:
            visible_name = _MISSING_DATABASE_NAME

        self.title(f'{_PROJECT_NAME} - {visible_name}')
