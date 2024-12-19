# p2app/views/countries.py
#
# ICS 33 Spring 2024
# Project 2: Learning to Fly
#
# This is the portion of the user interface that is displayed when the
# Edit / Countries menu item is selected.
#
# YOU WILL NOT NEED TO MODIFY THIS FILE AT ALL

import tkinter
import tkinter.messagebox
from p2app.events import *
from .event_handling import EventHandler
from .events import *



class CountriesView(tkinter.Frame, EventHandler):
    def __init__(self, parent):
        super().__init__(parent)

        search_view = _CountriesSearchView(self)
        search_view.grid(row = 0, column = 0, sticky = tkinter.NSEW)

        self._edit_view = None

        self.rowconfigure(0, weight = 0)
        self.rowconfigure(1, weight = 1)
        self.columnconfigure(0, weight = 1)


    def on_event(self, event):
        if isinstance(event, SaveCountryFailedEvent):
            tkinter.messagebox.showerror('Save Country Failed', event.reason())


    def on_event_post(self, event):
        if isinstance(event, DiscardCountryEvent):
            self._switch_edit_view(None)
        elif isinstance(event, NewCountryEvent):
            self._switch_edit_view(_CountryEditorView(self, True, True, None))
        elif isinstance(event, StartEditingCountryEvent):
            self._switch_edit_view(_CountryEditorLoadingView(self))
        elif isinstance(event, CountryLoadedEvent):
            self._switch_edit_view(_CountryEditorView(self, False, True, event.country()))
        elif isinstance(event, CountrySavedEvent):
            self._switch_edit_view(_CountryEditorView(self, False, False, event.country()))


    def _switch_edit_view(self, edit_view):
        if self._edit_view:
            self._edit_view.destroy()
            self._edit_view = None

        if edit_view:
            self._edit_view = edit_view
            self._edit_view.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tkinter.NSEW)



class _CountriesSearchView(tkinter.LabelFrame, EventHandler):
    def __init__(self, parent):
        super().__init__(parent, text = 'Country Search')

        code_label = tkinter.Label(self, text = 'Country Code: ')
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

        self._search_country_ids = []

        button_frame = tkinter.Frame(self)
        button_frame.grid(row = 4, column = 2, sticky = tkinter.E, padx = 5, pady = 5)

        self._new_button = tkinter.Button(
            button_frame, text = 'New Country',
            command = self._on_new_country)

        self._new_button.grid(row = 0, column = 0, padx = 5, pady = 5)

        self._edit_button = tkinter.Button(
            button_frame, text = 'Edit Country', state = tkinter.DISABLED,
            command = self._on_edit_country)

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
        self.initiate_event(ClearCountriesSearchListEvent())
        self.initiate_event(StartCountrySearchEvent(self._get_search_code(), self._get_search_name()))


    def _get_search_code(self):
        code = self._search_code.get().strip()
        return code if len(code) > 0 else None


    def _get_search_name(self):
        name = self._search_name.get().strip()
        return name if len(name) > 0 else None


    def _get_selected_search_country_id(self):
        selection, *_ = self._search_list.curselection()
        return self._search_country_ids[selection]


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


    def _on_new_country(self):
        self.initiate_event(DiscardCountryEvent())
        self.initiate_event(NewCountryEvent())


    def _on_edit_country(self):
        self.initiate_event(DiscardCountryEvent())
        self.initiate_event(StartEditingCountryEvent())
        self.initiate_event(LoadCountryEvent(self._get_selected_search_country_id()))


    def on_event(self, event):
        if isinstance(event, ClearCountriesSearchListEvent):
            self._search_list.delete(0, tkinter.END)
            self._search_country_ids = []
            self._edit_button['state'] = tkinter.DISABLED
        elif isinstance(event, CountrySearchResultEvent):
            display_name = f'{event.country().country_code} - {event.country().name}'
            self._search_list.insert(tkinter.END, display_name)
            self._search_country_ids.append(event.country().country_id)



class _CountryEditorLoadingView(tkinter.LabelFrame, EventHandler):
    def __init__(self, parent):
        super().__init__(parent)

        loading_label = tkinter.Label(self, text = 'Loading...')
        loading_label.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tkinter.W)



class _CountryEditorView(tkinter.LabelFrame, EventHandler):
    def __init__(self, parent, is_new, is_editable, country):
        if is_new:
            frame_text = 'New Country'
        elif is_editable:
            frame_text = 'Edit Country'
        else:
            frame_text = 'Country Saved'

        super().__init__(parent, text = frame_text)

        self._is_new = is_new
        self._country_id = country.country_id if country else None
        code = country.country_code if country and country.country_code else ''
        name = country.name if country and country.name else ''
        continent_id = country.continent_id if country and country.continent_id else 0
        wikipedia_link = country.wikipedia_link if country and country.wikipedia_link else ''
        keywords = country.keywords if country and country.keywords else ''

        self._country_code = tkinter.StringVar()
        self._country_code.set(code)

        self._country_name = tkinter.StringVar()
        self._country_name.set(name)

        self._continent_id = tkinter.StringVar()
        self._continent_id.set(str(continent_id))

        self._wikipedia_link = tkinter.StringVar()
        self._wikipedia_link.set(wikipedia_link)

        self._keywords = tkinter.StringVar()
        self._keywords.set(keywords)

        country_id_label = tkinter.Label(self, text = 'Country ID: ')
        country_id_label.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tkinter.E)

        country_id_value_label_text = f'{self._country_id if self._country_id else "(New)"}'
        country_id_value_label = tkinter.Label(self, text = country_id_value_label_text)
        country_id_value_label.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = tkinter.W)

        code_label = tkinter.Label(self, text = 'Country Code: ')
        code_label.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tkinter.E)

        if is_editable:
            code_entry = tkinter.Entry(self, textvariable = self._country_code, width = 10)
        else:
            code_entry = tkinter.Label(self, textvariable = self._country_code)

        code_entry.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = tkinter.W)

        name_label = tkinter.Label(self, text = 'Name: ')
        name_label.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = tkinter.E)

        if is_editable:
            name_entry = tkinter.Entry(self, textvariable = self._country_name, width = 30)
        else:
            name_entry = tkinter.Label(self, textvariable = self._country_name)

        name_entry.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = tkinter.W)

        continent_id_label = tkinter.Label(self, text = 'Continent ID: ')
        continent_id_label.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = tkinter.E)

        if is_editable:
            continent_id_entry = tkinter.Entry(self, textvariable = self._continent_id, width = 10)
        else:
            continent_id_entry = tkinter.Label(self, textvariable = self._continent_id)

        continent_id_entry.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = tkinter.W)

        wikipedia_link_label = tkinter.Label(self, text = 'Wikipedia Link: ')
        wikipedia_link_label.grid(row = 4, column = 0, padx = 5, pady = 5, sticky = tkinter.E)

        if is_editable:
            wikipedia_link_entry = tkinter.Entry(self, textvariable = self._wikipedia_link, width = 50)
        else:
            wikipedia_link_entry = tkinter.Label(self, textvariable = self._wikipedia_link)

        wikipedia_link_entry.grid(row = 4, column = 1, padx = 5, pady = 5, sticky = tkinter.W)

        keywords_label = tkinter.Label(self, text = 'Keywords: ')
        keywords_label.grid(row = 5, column = 0, padx = 5, pady = 5, sticky = tkinter.E)

        if is_editable:
            keywords_entry = tkinter.Entry(self, textvariable = self._keywords, width = 50)
        else:
            keywords_entry = tkinter.Label(self, textvariable = self._keywords)

        keywords_entry.grid(row = 5, column = 1, padx = 5, pady = 5, sticky = tkinter.W)

        button_frame = tkinter.Frame(self)
        button_frame.grid(row = 7, column = 1, padx = 5, pady = 5, sticky = tkinter.SE)

        if is_editable:
            save_button = tkinter.Button(button_frame, text = 'Save', command = self._on_save)
            save_button.grid(row = 0, column = 0, padx = 5, pady = 5)

        discard_button = tkinter.Button(button_frame, text = 'Discard', command = self._on_discard)
        discard_button.grid(row = 0, column = 1, padx = 5, pady = 5)

        self.rowconfigure(0, weight = 0)
        self.rowconfigure(1, weight = 0)
        self.rowconfigure(2, weight = 0)
        self.rowconfigure(3, weight = 0)
        self.rowconfigure(4, weight = 0)
        self.rowconfigure(5, weight = 0)
        self.rowconfigure(6, weight = 1)
        self.rowconfigure(7, weight = 0)
        self.columnconfigure(0, weight = 0)
        self.columnconfigure(1, weight = 1)


    def _on_save(self):
        country = self._make_country()

        if country:
            if self._is_new:
                self.initiate_event(SaveNewCountryEvent(country))
            else:
                self.initiate_event(SaveCountryEvent(country))


    def _on_discard(self):
        self.initiate_event(DiscardCountryEvent())


    def _make_country(self):
        try:
            continent_id = int(self._continent_id.get())
        except ValueError:
            tkinter.messagebox.showerror('Save Country Failed', 'Continent ID must be an integer')
            return None

        return Country(
            self._country_id, self._country_code.get(), self._country_name.get(),
            continent_id, self._wikipedia_link.get(), self._keywords.get())
