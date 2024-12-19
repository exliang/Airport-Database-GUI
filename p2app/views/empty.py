# An empty user interface area, for use when the application first starts up.

import tkinter


class EmptyView(tkinter.Frame):
    def __init__(self, parent):
        super().__init__(parent)
