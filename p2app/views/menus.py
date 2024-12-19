# p2app/views/menus.py
#
# ICS 33 Spring 2024
# Project 2: Learning to Fly
#
# An implementation of the application's menus.
#
# YOU WILL NOT NEED TO MODIFY THIS FILE AT ALL

import tkinter
import tkinter.filedialog
from p2app.events import *
from .events import *
from .event_handling import EventHandler



_OPEN_DATABASE_DIALOG_TITLE = 'Open Database'



class BaseMenu(tkinter.Menu, EventHandler):
    def __init__(self, parent):
        super().__init__(parent, tearoff = 0)



class MainMenu(BaseMenu):
    def __init__(self, parent):
        super().__init__(parent)
        self.add_cascade(label = 'File', menu = FileMenu(self))
        self.add_cascade(label = 'Debug', menu = DebugMenu(self))


    def on_event(self, event):
        if isinstance(event, DatabaseOpenedEvent):
            self.insert_cascade(index = 1, label = 'Edit', menu = EditMenu(self))
        elif isinstance(event, DatabaseClosedEvent):
            self.delete('Edit')



class FileMenu(BaseMenu):
    def __init__(self, parent):
        super().__init__(parent)
        self.add_command(label = 'Open', state = tkinter.NORMAL, command = self._on_open)
        self.add_command(label = 'Close', state = tkinter.DISABLED, command = self._on_close)
        self.add_command(label = 'Exit', command = self._on_exit)


    def _on_open(self):
        open_path = tkinter.filedialog.askopenfilename(
            title = _OPEN_DATABASE_DIALOG_TITLE,
            initialdir = Path.cwd())

        if open_path:
            self.initiate_event(OpenDatabaseEvent(Path(open_path)))


    def _on_close(self):
        self.initiate_event(CloseDatabaseEvent())


    def _on_exit(self):
        self.initiate_event(QuitInitiatedEvent())


    def on_event(self, event):
        if isinstance(event, DatabaseOpenedEvent):
            self.entryconfig('Open', state = tkinter.DISABLED)
            self.entryconfig('Close', state = tkinter.NORMAL)
        elif isinstance(event, DatabaseClosedEvent):
            self.entryconfig('Open', state = tkinter.NORMAL)
            self.entryconfig('Close', state = tkinter.DISABLED)



class EditMenu(BaseMenu):
    def __init__(self, parent):
        super().__init__(parent)
        self.add_command(label = 'Continents', command = self._on_edit_continents)
        self.add_command(label = 'Countries', command = self._on_edit_countries)
        self.add_command(label = 'Regions', command = self._on_edit_regions)


    def _on_edit_continents(self):
        self.initiate_event(ShowEditContinentsViewEvent())


    def _on_edit_countries(self):
        self.initiate_event(ShowEditCountriesViewEvent())


    def _on_edit_regions(self):
        self.initiate_event(ShowEditRegionsViewEvent())



class DebugMenu(BaseMenu):
    def __init__(self, parent):
        super().__init__(parent)

        self._is_debug_mode = tkinter.IntVar(self, 0)

        self.add_checkbutton(
            label = 'Show Events', variable = self._is_debug_mode,
            command = self._on_change_show_events)


    def _on_change_show_events(self):
        if self._is_debug_mode.get():
            self.initiate_event(EnableDebugModeEvent())
        else:
            self.initiate_event(DisableDebugModeEvent())
