"""Controller class part of MVC"""
import pygame
from src.engine.event_manager import (
    EventManager,
    TickEvent,
    QuitEvent,
    Event,
    ClickEvent,
)
from src.engine.model import GameEngine


class Controller:
    """Controller class"""

    def __init__(self, ev_manager: EventManager, model: GameEngine):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
        self.ev_manager = ev_manager
        ev_manager.register_listener(self)
        self.model: GameEngine = model
        self.square_selected: tuple = ()
        self.player_clicks: list = []
        self.most_recent_valid_move_click: list = []

    def unregister(self) -> None:
        """Unregister the controller from the set of listeners"""
        self.ev_manager.unregister_listener(self)

    def notify(self, event_type: Event) -> None:
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
                    location: tuple = pygame.mouse.get_pos()
                    col, row = int(location[0] / 64), int(location[1] / 64)
                    # If click on same square in square_selected
                    if self.square_selected == (col, row) or col >= 8 or row >= 8:
                        self.square_selected = ()
                        self.player_clicks = []
                    else:
                        # If click on different square than the one in square_selected
                        self.square_selected = col, row
                        self.player_clicks.append(self.square_selected)
                        if len(self.player_clicks) == 2:
                            self.most_recent_valid_move_click = self.player_clicks
                            self.square_selected = ()
                            self.player_clicks = []
                            click_event = ClickEvent(self.most_recent_valid_move_click)
                            self.ev_manager.post(click_event)
