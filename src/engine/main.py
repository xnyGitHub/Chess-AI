"""Module that connects the MVC together"""

from src.engine.event_manager import EventManager
from src.engine.model import GameEngine
from src.engine.view import PygameView
from src.engine.controller import Controller


def run():
    """Main Entry point"""
    ev_manager = EventManager()
    gamemodel = GameEngine(ev_manager)
    keyboard = Controller(ev_manager, gamemodel)
    graphics = PygameView(ev_manager, gamemodel)
    gamemodel.run()


if __name__ == "__main__":
    run()
