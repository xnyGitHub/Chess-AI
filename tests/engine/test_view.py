"""Unit-testing for src\engine\view.py"""
from unittest.mock import MagicMock, patch

from src.engine.view import PygameView
from src.engine.event_manager import EventManager, QuitEvent, TickEvent
from src.engine.model import GameEngine


class TestPygameView:
    """Class for testing the view (PygameView)"""

    def test_initialise(self):
        """Test whether the pygame instance is inisitalised when instance is created"""
        # Arrange
        event_manager = EventManager()
        model = GameEngine(event_manager)

        # Act
        pygame_instance = PygameView(event_manager, model, testing=True)

        # Assert
        assert pygame_instance.initialised is True

    @patch("src.engine.view.pygame.quit")
    def test_notify_quit_event(self, mock_pygame_quit):
        """Test the notify function by posting an event through event manager"""
        # Arrange
        event_manager = EventManager()
        model = GameEngine(event_manager)
        pygame_instance = PygameView(event_manager, model, testing=True)

        # Act
        quit_event = QuitEvent()
        event_manager.post(quit_event)

        # Assert
        mock_pygame_quit.assert_called()

    @patch("src.engine.view.pygame.quit")
    def test_notify_quit_event_unregistered(self, mock_pygame_quit):
        """Test the notify function by posting an event through event manager"""
        # Arrange
        event_manager = EventManager()

        # Act
        quit_event = QuitEvent()
        event_manager.post(quit_event)

        # Assert
        mock_pygame_quit.assert_not_called()

    @patch("src.engine.view.PygameView.render")
    def test_notify_render(self, mock_render):
        """Test the notify function by posting an event through event manager"""
        # Arrange
        event_manager = EventManager()
        model = GameEngine(event_manager)
        pygame_instance = PygameView(event_manager, model, testing=True)

        # Act
        tick_event = TickEvent()
        event_manager.post(tick_event)

        # Assert
        mock_render.assert_called()

    def test_load_images(self):
        """Test whether the piece images are loaded"""
        # Arrange
        event_manager = EventManager()
        model = GameEngine(event_manager)
        pygame_instance = PygameView(event_manager, model, testing=True)

        # Act
        load_images = pygame_instance.load_images()

        # Assert
        expected_result = None
        assert load_images != expected_result

    @patch("src.engine.view.PygameView.initialise", MagicMock(return_value=False))
    def test_render_when_not_initialised(self):
        """Test that render is not called when pygame has not been initialised"""
        # Arrange
        event_manager = EventManager()
        model = GameEngine(event_manager)
        pygame_instance = PygameView(event_manager, model, testing=True)

        # Act
        # Act is patched out

        # Assert
        assert pygame_instance.render() is None

    @patch("src.engine.view.PygameView.draw_pieces")
    @patch("src.engine.view.PygameView.draw_board")
    def test_render_when_initialised(self, mock_draw_piece, mock_draw_board):
        """Test that render is called when view has been initialised"""
        # Arrange
        event_manager = EventManager()
        model = GameEngine(event_manager)
        pygame_instance = PygameView(event_manager, model, testing=True)

        pygame_instance.render(testing=True)

        # Assert
        mock_draw_piece.assert_called()
        mock_draw_board.assert_called()
