# p2app/views/regions.py
#
# ICS 33 Spring 2024
# Project 2: Learning to Fly
#
# This is the portion of the user interface that is displayed when the
# Edit / Regions menu item is selected.
#
# YOU WILL NOT NEED TO MODIFY THIS FILE AT ALL

import tkinter
import tkinter.messagebox
from p2app.events import *
from .event_handling import EventHandler
from .events import *



class RegionsView(tkinter.Frame, EventHandler):
    def __init__(self, parent):
        super().__init__(parent)

        search_view = _RegionsSearchView(self)
        search_view.grid(row = 0, column = 0, sticky = tkinter.NSEW)

        self._edit_view = None

        self.rowconfigure(0, weight = 0)
        self.rowconfigure(1, weight = 1)
        self.columnconfigure(0, weight = 1)


    def on_event(self, event):
        if isinstance(event, SaveRegionFailedEvent):
            tkinter.messagebox.showerror('Save Region Failed', event.reason())


    def on_event_post(self, event):
        if isinstance(event, DiscardRegionEvent):
            self._switch_edit_view(None)
        elif isinstance(event, NewRegionEvent):
            self._switch_edit_view(_RegionEditorView(self, True, True, None))
        elif isinstance(event, StartEditingRegionEvent):
            self._switch_edit_view(_RegionEditorLoadingView(self))
        elif isinstance(event, RegionLoadedEvent):
            self._switch_edit_view(_RegionEditorView(self, False, True, event.region()))
        elif isinstance(event, RegionSavedEvent):
            self._switch_edit_view(_RegionEditorView(self, False, False, event.region()))


    def _switch_edit_view(self, edit_view):
        if self._edit_view:
            self._edit_view.destroy()
            self._edit_view = None

        if edit_view:
            self._edit_view = edit_view
            self._edit_view.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tkinter.NSEW)



class _RegionsSearchView(tkinter.LabelFrame, EventHandler):
    def __init__(self, parent):
        super().__init__(parent, text = 'Region Search')

        region_code_label = tkinter.Label(self, text = 'Region Code: ')
        region_code_label.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tkinter.E)

        self._search_region_code = tkinter.StringVar()
        self._search_region_code.trace_add('write', self._on_search_changed)

        region_code_entry = tkinter.Entry(self, textvariable = self._search_region_code, width = 10)
        region_code_entry.grid(row = 0, column = 1, sticky = tkinter.W, padx = 5, pady = 5)

        local_code_label = tkinter.Label(self, text = 'Local Code: ')
        local_code_label.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tkinter.E)

        self._search_local_code = tkinter.StringVar()
        self._search_local_code.trace_add('write', self._on_search_changed)

        local_code_entry = tkinter.Entry(self, textvariable = self._search_local_code, width = 10)
        local_code_entry.grid(row = 1, column = 1, sticky = tkinter.W, padx = 5, pady = 5)

        name_label = tkinter.Label(self, text = 'Name: ')
        name_label.grid(row = 2, column = 0, sticky = tkinter.E, padx = 5, pady = 5)

        self._search_name = tkinter.StringVar()
        self._search_name.trace_add('write', self._on_search_changed)

        name_entry = tkinter.Entry(self, textvariable = self._search_name, width = 30)
        name_entry.grid(row = 2, column = 1, sticky = tkinter.EW, padx = 5, pady = 5)

        self._search_button = tkinter.Button(
            self, text = 'Search', state = tkinter.DISABLED,
            command = self._on_search_button_clicked)

        self._search_button.grid(row = 3, column = 1, sticky = tkinter.E, padx = 5, pady = 5)

        empty_area = tkinter.Label(self, text = '')
        empty_area.grid(row = 4, column = 1, sticky = tkinter.NSEW, padx = 5, pady = 5)

        self._search_list = tkinter.Listbox(
            self, height = 4,
            activestyle = tkinter.NONE, selectmode = tkinter.SINGLE)

        self._search_list.bind('<<ListboxSelect>>', self._on_search_selection_changed)
        self._search_list.grid(
            row = 0, column = 2, rowspan = 4, columnspan = 1, sticky = tkinter.NSEW,
            padx = 5, pady = 5)

        self._search_region_ids = []

        button_frame = tkinter.Frame(self)
        button_frame.grid(row = 5, column = 2, sticky = tkinter.E, padx = 5, pady = 5)

        self._new_button = tkinter.Button(
            button_frame, text = 'New Region',
            command = self._on_new_region)

        self._new_button.grid(row = 0, column = 0, padx = 5, pady = 5)

        self._edit_button = tkinter.Button(
            button_frame, text = 'Edit Region', state = tkinter.DISABLED,
            command = self._on_edit_region)

        self._edit_button.grid(row = 0, column = 1, padx = 5, pady = 5)

        self.rowconfigure(0, weight = 0)
        self.rowconfigure(1, weight = 0)
        self.rowconfigure(2, weight = 0)
        self.rowconfigure(3, weight = 0)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 0)
        self.columnconfigure(0, weight = 0)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 2)


    def _on_search_button_clicked(self):
        self.initiate_event(ClearRegionsSearchListEvent())
        self.initiate_event(StartRegionSearchEvent(
            self._get_search_region_code(), self._get_search_local_code(),
            self._get_search_name()))


    def _get_search_region_code(self):
        code = self._search_region_code.get().strip()
        return code if len(code) > 0 else None


    def _get_search_local_code(self):
        code = self._search_local_code.get().strip()
        return code if len(code) > 0 else None


    def _get_search_name(self):
        name = self._search_name.get().strip()
        return name if len(name) > 0 else None


    def _get_selected_search_region_id(self):
        selection, *_ = self._search_list.curselection()
        return self._search_region_ids[selection]


    def _on_search_changed(self, *args):
        if len(self._search_region_code.get().strip()) > 0 \
                or len(self._search_local_code.get().strip()) > 0 \
                or len(self._search_name.get().strip()) > 0:
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


    def _on_new_region(self):
        self.initiate_event(DiscardRegionEvent())
        self.initiate_event(NewRegionEvent())


    def _on_edit_region(self):
        self.initiate_event(DiscardRegionEvent())
        self.initiate_event(StartEditingRegionEvent())
        self.initiate_event(LoadRegionEvent(self._get_selected_search_region_id()))


    def on_event(self, event):
        if isinstance(event, ClearRegionsSearchListEvent):
            self._search_list.delete(0, tkinter.END)
            self._search_region_ids = []
            self._edit_button['state'] = tkinter.DISABLED
        elif isinstance(event, RegionSearchResultEvent):
            display_name = f'{event.region().region_code} - {event.region().name}'
            self._search_list.insert(tkinter.END, display_name)
            self._search_region_ids.append(event.region().region_id)



class _RegionEditorLoadingView(tkinter.LabelFrame, EventHandler):
    def __init__(self, parent):
        super().__init__(parent)

        loading_label = tkinter.Label(self, text = 'Loading...')
        loading_label.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tkinter.W)



class _RegionEditorView(tkinter.LabelFrame, EventHandler):
    def __init__(self, parent, is_new, is_editable, region):
        if is_new:
            frame_text = 'New Region'
        elif is_editable:
            frame_text = 'Edit Region'
        else:
            frame_text = 'Region Saved'

        super().__init__(parent, text = frame_text)

        self._is_new = is_new
        self._region_id = region.region_id if region else None
        region_code = region.region_code if region and region.region_code else ''
        local_code = region.local_code if region and region.local_code else ''
        name = region.name if region and region.name else ''
        continent_id = region.continent_id if region and region.continent_id else 0
        country_id = region.country_id if region and region.country_id else 0
        wikipedia_link = region.wikipedia_link if region and region.wikipedia_link else ''
        keywords = region.keywords if region and region.keywords else ''

        self._region_code = tkinter.StringVar()
        self._region_code.set(region_code)

        self._local_code = tkinter.StringVar()
        self._local_code.set(local_code)

        self._region_name = tkinter.StringVar()
        self._region_name.set(name)

        self._continent_id = tkinter.StringVar()
        self._continent_id.set(str(continent_id))

        self._country_id = tkinter.StringVar()
        self._country_id.set(str(country_id))

        self._wikipedia_link = tkinter.StringVar()
        self._wikipedia_link.set(wikipedia_link)

        self._keywords = tkinter.StringVar()
        self._keywords.set(keywords)

        region_id_label = tkinter.Label(self, text = 'Region ID: ')
        region_id_label.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tkinter.E)

        region_id_value_label_text = f'{self._region_id if self._region_id else "(New)"}'
        region_id_value_label = tkinter.Label(self, text = region_id_value_label_text)
        region_id_value_label.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = tkinter.W)

        region_code_label = tkinter.Label(self, text = 'Region Code: ')
        region_code_label.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tkinter.E)

        if is_editable:
            region_code_entry = tkinter.Entry(self, textvariable = self._region_code, width = 10)
        else:
            region_code_entry = tkinter.Label(self, textvariable = self._region_code)

        region_code_entry.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = tkinter.W)

        local_code_label = tkinter.Label(self, text = 'Local Code: ')
        local_code_label.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = tkinter.E)

        if is_editable:
            local_code_entry = tkinter.Entry(self, textvariable = self._local_code, width = 10)
        else:
            local_code_entry = tkinter.Label(self, textvariable = self._local_code)

        local_code_entry.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = tkinter.W)

        name_label = tkinter.Label(self, text = 'Name: ')
        name_label.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = tkinter.E)

        if is_editable:
            name_entry = tkinter.Entry(self, textvariable = self._region_name, width = 30)
        else:
            name_entry = tkinter.Label(self, textvariable = self._region_name)

        name_entry.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = tkinter.W)

        continent_id_label = tkinter.Label(self, text = 'Continent ID: ')
        continent_id_label.grid(row = 4, column = 0, padx = 5, pady = 5, sticky = tkinter.E)

        if is_editable:
            continent_id_entry = tkinter.Entry(self, textvariable = self._continent_id, width = 10)
        else:
            continent_id_entry = tkinter.Label(self, textvariable = self._continent_id)

        continent_id_entry.grid(row = 4, column = 1, padx = 5, pady = 5, sticky = tkinter.W)

        country_id_label = tkinter.Label(self, text = 'Country ID: ')
        country_id_label.grid(row = 5, column = 0, padx = 5, pady = 5, sticky = tkinter.E)

        if is_editable:
            country_id_entry = tkinter.Entry(self, textvariable = self._country_id, width = 10)
        else:
            country_id_entry = tkinter.Label(self, textvariable = self._country_id)

        country_id_entry.grid(row = 5, column = 1, padx = 5, pady = 5, sticky = tkinter.W)

        wikipedia_link_label = tkinter.Label(self, text = 'Wikipedia Link: ')
        wikipedia_link_label.grid(row = 6, column = 0, padx = 5, pady = 5, sticky = tkinter.E)

        if is_editable:
            wikipedia_link_entry = tkinter.Entry(self, textvariable = self._wikipedia_link, width = 50)
        else:
            wikipedia_link_entry = tkinter.Label(self, textvariable = self._wikipedia_link)

        wikipedia_link_entry.grid(row = 6, column = 1, padx = 5, pady = 5, sticky = tkinter.W)

        keywords_label = tkinter.Label(self, text = 'Keywords: ')
        keywords_label.grid(row = 7, column = 0, padx = 5, pady = 5, sticky = tkinter.E)

        if is_editable:
            keywords_entry = tkinter.Entry(self, textvariable = self._keywords, width = 50)
        else:
            keywords_entry = tkinter.Label(self, textvariable = self._keywords)

        keywords_entry.grid(row = 7, column = 1, padx = 5, pady = 5, sticky = tkinter.W)

        button_frame = tkinter.Frame(self)
        button_frame.grid(row = 9, column = 1, padx = 5, pady = 5, sticky = tkinter.SE)

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
        self.rowconfigure(6, weight = 0)
        self.rowconfigure(7, weight = 0)
        self.rowconfigure(8, weight = 1)
        self.rowconfigure(9, weight = 0)
        self.columnconfigure(0, weight = 0)
        self.columnconfigure(1, weight = 1)


    def _on_save(self):
        region = self._make_region()

        if region:
            if self._is_new:
                self.initiate_event(SaveNewRegionEvent(region))
            else:
                self.initiate_event(SaveRegionEvent(region))


    def _on_discard(self):
        self.initiate_event(DiscardRegionEvent())


    def _make_region(self):
        failure_reasons = []

        try:
            continent_id = int(self._continent_id.get())
        except ValueError:
            failure_reasons.append('Continent ID must be an integer')

        try:
            country_id = int(self._country_id.get())
        except ValueError:
            failure_reasons.append('Country ID must be an integer')

        if failure_reasons:
            tkinter.messagebox.showerror('Save Region Failed', '\n'.join(failure_reasons))
            return None
        else:
            return Region(
                self._region_id, self._region_code.get(), self._local_code.get(),
                self._region_name.get(), continent_id, country_id,
                self._wikipedia_link.get(), self._keywords.get())
