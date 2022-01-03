"""Controller class part of MVC"""
import pygame
from src.engine.event_manager import TickEvent, QuitEvent, Event, ClickEvent


class Controller:
    """Controller class"""

    def __init__(self, ev_manager, model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
        self.ev_manager = ev_manager
        ev_manager.register_listener(self)
        self.model = model

    def unregister(self):
        """Unregister the controller from the set of listeners"""
        self.ev_manager.unregister_listener(self)

    def notify(self, event_type):
        """
        Receive events posted to the message queue.
        """
        # pylint: disable=no-member
        if isinstance(event_type, TickEvent):

            # Called for each game tick. We check our keyboard presses here.
            for event in pygame.event.get():
                # Handle click on close
                if event.type == pygame.QUIT:
                    self.ev_manager.post(QuitEvent())
                # Handle Key events
                if event.type == pygame.KEYDOWN:
                    self.ev_manager.post(Event())
                # Handle Mouse Button events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    location = (
                        pygame.mouse.get_pos()
                    )  # We get the pixel location of mouse
                    # pygame.event.post(test_event)
                    click_event = ClickEvent(location)
                    self.ev_manager.post(click_event)
