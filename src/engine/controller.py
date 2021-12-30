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

    def notify(self, event_type):
        """
        Receive events posted to the message queue.
        """
        # if isinstance(event_type, TickEvent) and event_type.testing:
        #     test_event = pygame.event.Event(
        #         pygame.MOUSEBUTTONDOWN, {"pos": (245, 221), "button": 1}
        #     )
        #     pygame.event.post(test_event)

        if isinstance(event_type, TickEvent):

            # Called for each game tick. We check our keyboard presses here.
            for event in pygame.event.get():
                # handle window manager closing our window
                if event.type == pygame.QUIT:
                    self.ev_manager.post(QuitEvent())
                # handle key down events
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.ev_manager.post(QuitEvent())
                    else:
                        # post any other keys to the message queue for everyone else to see
                        self.ev_manager.post(Event())
                if event.type == pygame.MOUSEBUTTONDOWN:
                    location = (
                        pygame.mouse.get_pos()
                    )  # We get the pixel location of mouse
                    # pygame.event.post(test_event)
                    click_event = ClickEvent(location)
                    self.ev_manager.post(click_event)
