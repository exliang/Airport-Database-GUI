from p2app import EventBus
from p2app import Engine
from p2app import MainView


def main():
    event_bus = EventBus()
    engine = Engine()
    main_view = MainView(event_bus)

    event_bus.register_engine(engine)
    event_bus.register_view(main_view)

    main_view.run()


if __name__ == '__main__':
    main()
