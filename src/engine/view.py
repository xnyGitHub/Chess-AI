"""View class as part of MVC model"""
import pygame
from src.engine.event_types import QuitEvent


class PygameView:
    """Pygame UI class"""

    def __init__(self, ev_manager):
        """Constructor"""

        self.ev_manager = ev_manager
        ev_manager.register_listener(self)

        self.initialised = False
        self.screen = None
        self.clock = None

    def initialise(self):
        """Create and initialise a pygame instance"""

        pygame.init()
        pygame.display.set_caption("Chess Engine")

        self.screen = pygame.display.set_mode((512, 512))
        self.clock = pygame.time.Clock()
        self.initialised = True

    def render(self):
        """Render the screen"""
        if not self.initialised:
            return

        # Implement screen refresh/update/render here after return statement

    def notify(self, event):
        """Process the event and decide what to do"""
        if isinstance(event, QuitEvent):
            self.initialised = False
            pygame.quit()

        # Process all other events here
