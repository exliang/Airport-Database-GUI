# p2app/views/continents.py
#
# ICS 33 Spring 2024
# Project 2: Learning to Fly
#
# This is the portion of the user interface that is displayed when the
# Edit / Continents menu item is selected.
#
# YOU WILL NOT NEED TO MODIFY THIS FILE AT ALL

import tkinter
import tkinter.messagebox
from p2app.events import *
from .event_handling import EventHandler
from .events import *



class ContinentsView(tkinter.Frame, EventHandler):
    def __init__(self, parent):
        super().__init__(parent)

        search_view = _ContinentsSearchView(self)
        search_view.grid(row = 0, column = 0, sticky = tkinter.NSEW)

        self._edit_view = None

        self.rowconfigure(0, weight = 0)
        self.rowconfigure(1, weight = 1)
        self.columnconfigure(0, weight = 1)


    def on_event(self, event):
        if isinstance(event, SaveContinentFailedEvent):
            tkinter.messagebox.showerror('Save Continent Failed', event.reason())


    def on_event_post(self, event):
        if isinstance(event, DiscardContinentEvent):
            self._switch_edit_view(None)
        elif isinstance(event, NewContinentEvent):
            self._switch_edit_view(_ContinentEditorView(self, True, True, None))
        elif isinstance(event, StartEditingContinentEvent):
            self._switch_edit_view(_ContinentEditorLoadingView(self))
        elif isinstance(event, ContinentLoadedEvent):
            self._switch_edit_view(_ContinentEditorView(self, False, True, event.continent()))
        elif isinstance(event, ContinentSavedEvent):
            self._switch_edit_view(_ContinentEditorView(self, False, False, event.continent()))


    def _switch_edit_view(self, edit_view):
        if self._edit_view:
            self._edit_view.destroy()
            self._edit_view = None

        if edit_view:
            self._edit_view = edit_view
            self._edit_view.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tkinter.NSEW)


class _ContinentsSearchView(tkinter.LabelFrame, EventHandler):
    def __init__(self, parent):
        super().__init__(parent, text = 'Continent Search')

        code_label = tkinter.Label(self, text = 'Continent Code: ')
        code_label.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tkinter.E)

        self._search_code = tkinter.StringVar()
        self._search_code.trace_add('write', self._on_search_changed)

        code_entry = tkinter.Entry(self, textvariable = self._search_code, width = 10)
        code_entry.grid(row = 0, column = 1, sticky = tkinter.W, padx = 5, pady = 5)

        name_label = tkinter.Label(self, text = 'Name: ')
        name_label.grid(row = 1, column = 0, sticky = tkinter.E, padx = 5, pady = 5)

        self._search_name = tkinter.StringVar()
        self._search_name.trace_add('write', self._on_search_changed)

        name_entry = tkinter.Entry(self, textvariable = self._search_name, width = 30)
        name_entry.grid(row = 1, column = 1, sticky = tkinter.EW, padx = 5, pady = 5)

        self._search_button = tkinter.Button(
            self, text = 'Search', state = tkinter.DISABLED,
            command = self._on_search_button_clicked)

        self._search_button.grid(row = 2, column = 1, sticky = tkinter.E, padx = 5, pady = 5)

        empty_area = tkinter.Label(self, text = '')
        empty_area.grid(row = 3, column = 1, sticky = tkinter.NSEW, padx = 5, pady = 5)

        self._search_list = tkinter.Listbox(
            self, height = 4,
            activestyle = tkinter.NONE, selectmode = tkinter.SINGLE)

        self._search_list.bind('<<ListboxSelect>>', self._on_search_selection_changed)
        self._search_list.grid(
            row = 0, column = 2, rowspan = 4, columnspan = 1, sticky = tkinter.NSEW,
            padx = 5, pady = 5)

        self._search_continent_ids = []

        button_frame = tkinter.Frame(self)
        button_frame.grid(row = 4, column = 2, sticky = tkinter.E, padx = 5, pady = 5)

        self._new_button = tkinter.Button(
            button_frame, text = 'New Continent',
            command = self._on_new_continent)

        self._new_button.grid(row = 0, column = 0, padx = 5, pady = 5)

        self._edit_button = tkinter.Button(
            button_frame, text = 'Edit Continent', state = tkinter.DISABLED,
            command = self._on_edit_continent)

        self._edit_button.grid(row = 0, column = 1, padx = 5, pady = 5)

        self.rowconfigure(0, weight = 0)
        self.rowconfigure(1, weight = 0)
        self.rowconfigure(2, weight = 0)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 0)
        self.columnconfigure(0, weight = 0)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 2)


    def _on_search_button_clicked(self):
        self.initiate_event(ClearContinentsSearchListEvent())
        self.initiate_event(StartContinentSearchEvent(self._get_search_code(), self._get_search_name()))


    def _get_search_code(self):
        code = self._search_code.get().strip()
        return code if len(code) > 0 else None


    def _get_search_name(self):
        name = self._search_name.get().strip()
        return name if len(name) > 0 else None


    def _get_selected_search_continent_id(self):
        selection, *_ = self._search_list.curselection()
        return self._search_continent_ids[selection]


    def _on_search_changed(self, *args):
        if len(self._search_code.get().strip()) > 0 or len(self._search_name.get().strip()) > 0:
            new_state = tkinter.NORMAL
        else:
            new_state = tkinter.DISABLED

        self._search_button['state'] = new_state
        return True


    def _on_search_selection_changed(self, event):
        if event.widget.curselection():
            new_state = tkinter.NORMAL
        else:
            new_state = tkinter.DISABLED

        self._edit_button['state'] = new_state


    def _on_new_continent(self):
        self.initiate_event(DiscardContinentEvent())
        self.initiate_event(NewContinentEvent())


    def _on_edit_continent(self):
        self.initiate_event(DiscardContinentEvent())
        self.initiate_event(StartEditingContinentEvent())
        self.initiate_event(LoadContinentEvent(self._get_selected_search_continent_id()))


    def on_event(self, event):
        if isinstance(event, ClearContinentsSearchListEvent):
            self._search_list.delete(0, tkinter.END)
            self._search_continent_ids = []
            self._edit_button['state'] = tkinter.DISABLED
        elif isinstance(event, ContinentSearchResultEvent):
            display_name = f'{event.continent().continent_code} - {event.continent().name}'
            self._search_list.insert(tkinter.END, display_name)
            self._search_continent_ids.append(event.continent().continent_id)



class _ContinentEditorLoadingView(tkinter.LabelFrame, EventHandler):
    def __init__(self, parent):
        super().__init__(parent)

        loading_label = tkinter.Label(self, text = 'Loading...')
        loading_label.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tkinter.W)



class _ContinentEditorView(tkinter.LabelFrame, EventHandler):
    def __init__(self, parent, is_new, is_editable, continent):
        if is_new:
            frame_text = 'New Continent'
        elif is_editable:
            frame_text = 'Edit Continent'
        else:
            frame_text = 'Continent Saved'

        super().__init__(parent, text = frame_text)

        self._is_new = is_new
        self._continent_id = continent.continent_id if continent else None
        code = continent.continent_code if continent and continent.continent_code else ''
        name = continent.name if continent and continent.name else ''

        self._continent_code = tkinter.StringVar()
        self._continent_code.set(code)

        self._continent_name = tkinter.StringVar()
        self._continent_name.set(name)

        continent_id_label = tkinter.Label(self, text = 'Continent ID: ')
        continent_id_label.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tkinter.E)

        continent_id_value_label_text = f'{self._continent_id if self._continent_id else "(New)"}'
        continent_id_value_label = tkinter.Label(self, text = continent_id_value_label_text)
        continent_id_value_label.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = tkinter.W)

        code_label = tkinter.Label(self, text = 'Continent Code: ')
        code_label.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tkinter.E)

        if is_editable:
            code_entry = tkinter.Entry(self, textvariable = self._continent_code, width = 10)
        else:
            code_entry = tkinter.Label(self, textvariable = self._continent_code)

        code_entry.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = tkinter.W)

        name_label = tkinter.Label(self, text = 'Name: ')
        name_label.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = tkinter.E)

        if is_editable:
            name_entry = tkinter.Entry(self, textvariable = self._continent_name, width = 30)
        else:
            name_entry = tkinter.Label(self, textvariable = self._continent_name)

        name_entry.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = tkinter.W)

        button_frame = tkinter.Frame(self)
        button_frame.grid(row = 4, column = 1, padx = 5, pady = 5, sticky = tkinter.SE)

        if is_editable:
            save_button = tkinter.Button(button_frame, text = 'Save', command = self._on_save)
            save_button.grid(row = 0, column = 0, padx = 5, pady = 5)

        discard_button = tkinter.Button(button_frame, text = 'Discard', command = self._on_discard)
        discard_button.grid(row = 0, column = 1, padx = 5, pady = 5)

        self.rowconfigure(0, weight = 0)
        self.rowconfigure(1, weight = 0)
        self.rowconfigure(2, weight = 0)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 0)
        self.columnconfigure(0, weight = 0)
        self.columnconfigure(1, weight = 1)


    def _on_save(self):
        if self._is_new:
            self.initiate_event(SaveNewContinentEvent(self._make_continent()))
        else:
            self.initiate_event(SaveContinentEvent(self._make_continent()))


    def _on_discard(self):
        self.initiate_event(DiscardContinentEvent())


    def _make_continent(self):
        return Continent(self._continent_id, self._continent_code.get(), self._continent_name.get())
