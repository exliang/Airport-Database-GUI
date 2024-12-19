# project2.py
#
# ICS 33 Spring 2024
# Project 2: Learning to Fly
#
# This is the main module that runs the entire program.
#
# YOU WILL NOT NEED TO MODIFY THIS FILE AT ALL

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