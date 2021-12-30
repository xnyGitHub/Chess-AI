"""View class as part of MVC model"""
import pygame
from src.engine.event_manager import QuitEvent, TickEvent


WIDTH = HEIGHT = 512  # Heigh and width of the board
DIMENSION = 8  # This will cause 8 squares to be print on the board
SQUARE_SIZE = HEIGHT / DIMENSION  # Dimensions of the square


class PygameView:
    """Pygame UI class"""

    def __init__(self, ev_manager, model, testing: bool = False):
        """Constructor"""

        self.ev_manager = ev_manager
        ev_manager.register_listener(self)
        self.model = model

        self.initialised = False
        self.screen = None
        self.clock = None
        self.images = {}
        self.initialised = self.initialise(testing)

    def notify(self, event):
        """Process the event and decide what to do"""
        if isinstance(event, QuitEvent):
            self.initialised = False
            pygame.quit()
        if isinstance(event, TickEvent):
            self.render()
        # Process all other events here

    def load_images(self):
        """Load the images into a dictionary"""
        pieces = [
            "wP",
            "wR",
            "wN",
            "wB",
            "wQ",
            "wK",
            "bP",
            "bR",
            "bN",
            "bB",
            "bK",
            "bQ",
        ]
        for piece in pieces:
            self.images[piece] = pygame.image.load(
                "src/assets/images/" + piece + ".png"
            )

        return self.images

    def render(self, testing: bool = False):
        """Render the screen"""
        if not self.initialised:
            return

        self.draw_board()
        self.draw_pieces()
        if not testing:
            pygame.display.flip()

    def draw_board(self):
        """Functions that draws the board without the pieces
        pygame.draw.rect() -> Draw rectangle on given surface
        pygame.draw.rect(surface,color,Rect)

        pygame.Rect() -> Pygame object for storing rectangular coordinates
        pygame.Rect(left(x-cord), top(y-cord), width, height)

        """
        colors = [pygame.Color("white"), pygame.Color("gray")]
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                color = colors[((row + col) % 2)]
                pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(
                        col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE
                    ),
                )

    def draw_pieces(self):
        """Draw the piece images onto the board"""
        board = self.model.board
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                piece = board[row][col]
                if piece != "--":
                    self.screen.blit(
                        self.images[piece],
                        pygame.Rect(
                            col * SQUARE_SIZE,
                            row * SQUARE_SIZE,
                            SQUARE_SIZE,
                            SQUARE_SIZE,
                        ),
                    )

    def initialise(self, testing: bool = False):
        """Create and initialise a pygame instance"""

        if not testing:

            pygame.display.set_caption("Chess Engine")
            self.screen = pygame.display.set_mode((512, 512))
            self.clock = pygame.time.Clock()
            self.load_images()

        return True
