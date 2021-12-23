"""Controller class part of MVC"""
import pygame
from src.engine.event_types import TickEvent, QuitEvent, Event


class KeyboardAndMouse:
    """Controller class"""

    def __init__(self, ev_manager, model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
        self.ev_manager = ev_manager
        ev_manager.register_listener(self)
        self.model = model

    def notify(self, event):
        """
        Receive events posted to the message queue.
        """

        if isinstance(event, TickEvent):
            # Called for each game tick. We check our keyboard presses here.
            for pyg_ev in pygame.event.get():
                # handle window manager closing our window
                if pyg_ev.type == pygame.QUIT:
                    self.ev_manager.post(QuitEvent())
                # handle key down events
                if pyg_ev.type == pygame.KEYDOWN:
                    if pyg_ev.key == pygame.K_ESCAPE:
                        self.ev_manager.post(QuitEvent())
                    else:
                        # post any other keys to the message queue for everyone else to see
                        self.ev_manager.post(Event())
