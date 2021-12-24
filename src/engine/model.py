"""Model class part of the MVC"""
from src.engine.event_types import QuitEvent, TickEvent
from src.engine.board import GameState


class GameEngine:
    """Holds the game state."""

    def __init__(self, ev_manager):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        Attributes:
        running (bool): True while the engine is online. Changed via QuitEvent().
        """

        self.ev_manager = ev_manager
        ev_manager.register_listener(self)
        self.running = False
        self.gamestate = GameState()

    def notify(self, event):
        """Called by an event in the message queue."""

        if isinstance(event, QuitEvent):
            self.running = False

    def run(self):
        """
        Starts the game engine loop.
        This pumps a Tick event into the message queue for each loop.
        The loop ends when this object hears a QuitEvent in notify().
        """
        self.running = True
        while self.running:
            new_tick = TickEvent()
            self.ev_manager.post(new_tick)
