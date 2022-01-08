"""View class as part of MVC model"""
import pygame
from src.engine.event_manager import Event, QuitEvent, TickEvent, EventManager
from src.engine.model import GameEngine


WIDTH = HEIGHT = 512  # Heigh and width of the board
DIMENSION = 8  # This will cause 8 squares to be print on the board
SQUARE_SIZE = HEIGHT / DIMENSION  # Dimensions of the square


class PygameView:
    """Pygame UI class"""

    def __init__(self, ev_manager: EventManager, model: GameEngine):
        """Constructor"""

        self.ev_manager: EventManager = ev_manager
        ev_manager.register_listener(self)
        self.model: GameEngine = model

        self.initialised: bool = False
        self.screen: pygame.Surface = None
        self.images: dict = {}
        self.initialised: bool = self.initialise()

    def notify(self, event: Event):
        """Process the event and decide what to do"""
        if isinstance(event, QuitEvent):
            self.initialised = False
            pygame.quit()  # pylint: disable=no-member
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

    def render(self):
        """Render the screen"""
        if not self.initialised:
            return

        self.draw_board()
        self.draw_pieces()
        self.draw_files_and_rank()
        pygame.display.flip()

    def draw_board(self):
        """Functions that draws the board without the pieces
        pygame.draw.rect() -> Draw rectangle on given surface
        pygame.draw.rect(surface,color,Rect)

        pygame.Rect() -> Pygame object for storing rectangular coordinates
        pygame.Rect(left(x-cord), top(y-cord), width, height)

        """
        off_green: tuple = (119, 149, 86)
        off_white: tuple = (235, 235, 208)
        colors: list = [off_white, off_green]
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
        board: list = self.model.board
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

    def draw_files_and_rank(self):
        """Draw the ranks and file"""
        pygame.font.init()
        font: pygame.font.Font = pygame.font.Font(pygame.font.get_default_font(), 12)
        files: list = ["0", "1", "2", "3", "4", "5", "6", "7"]
        for index in range(DIMENSION):  # Loop through each rank
            text_object = font.render(files[index], True, pygame.Color("Black"))
            self.screen.blit(
                text_object,
                pygame.Rect(3, index * SQUARE_SIZE + 3, SQUARE_SIZE, SQUARE_SIZE),
            )
            self.screen.blit(
                text_object,
                pygame.Rect(
                    index * SQUARE_SIZE + 52, 512 - 15, SQUARE_SIZE, SQUARE_SIZE
                ),
            )  # Measurements to display the ranks

    def initialise(self):
        """Create and initialise a pygame instance"""

        # pylint: disable=no-member
        pygame.init()
        # pylint: enable=no-member

        pygame.display.set_caption("Chess Engine")
        self.screen: pygame.Surface = pygame.display.set_mode((512, 512))

        self.load_images()

        return True
