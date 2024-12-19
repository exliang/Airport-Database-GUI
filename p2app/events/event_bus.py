class EventBus:
    def __init__(self):
        self._view = None
        self._engine = None
        self._is_debug_mode = False

    def register_view(self, view):
        self._view = view

    def register_engine(self, engine):
        self._engine = engine

    def enable_debug_mode(self):
        self._is_debug_mode = True

    def disable_debug_mode(self):
        self._is_debug_mode = False

    def initiate_event(self, event):
        if self._is_debug_mode:
            print(f'Sent by view  : {event}')

        for result_event in self._engine.process_event(event):
            if self._is_debug_mode:
                print(f'Sent by engine: {result_event}')

            self._view.handle_event(result_event)
