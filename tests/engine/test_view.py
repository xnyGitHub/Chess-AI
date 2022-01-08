"""Unit-testing for src/engine/view.py"""  # pylint: disable=no-member,attribute-defined-outside-init,unused-variable,too-few-public-methods
from unittest import mock

from src.engine.view import PygameView
from src.engine.event_manager import EventManager, QuitEvent, TickEvent
from src.engine.model import GameEngine


class TestPygameView:
    """Class for testing the view (PygameView)"""

    def setup_method(self):
        """Setup method that mocks out pygame initialisation"""
        patch = mock.patch("src.engine.view.pygame.init")
        self.mock_py_init = patch.start()
        patch = mock.patch("src.engine.view.pygame.display.set_mode")
        self.mock_py_set_mode = patch.start()
        patch = mock.patch("src.engine.view.pygame.display.set_caption")
        self.mock_py_set_caption = patch.start()
        print("Setup running...")

    def teardown_method(self):
        """Tear down method that stops the mocks"""
        print("Teardown running...")
        mock.patch.stopall()

    def test_initialise(self):
        """Test whether the pygame instance is inisitalised when instance is created"""
        # Arrange
        event_manager = EventManager()
        model = GameEngine(event_manager)

        # Act
        pygame_instance = PygameView(event_manager, model)

        # Assert
        assert pygame_instance.initialised is True
        self.mock_py_set_mode.assert_called()
        self.mock_py_set_caption.assert_called()

    @mock.patch("src.engine.view.pygame.quit")
    def test_notify_quit_event(self, mock_pygame_quit):
        """Test the notify function by posting an event through event manager"""
        # Arrange
        event_manager = EventManager()
        model = GameEngine(event_manager)
        pygame_instance = PygameView(event_manager, model)

        # Act
        quit_event = QuitEvent()
        event_manager.post(quit_event)

        # Assert
        mock_pygame_quit.assert_called()

    @mock.patch("src.engine.view.pygame.quit")
    def test_notify_quit_event_unregistered(self, mock_pygame_quit):
        """Test the notify function by posting an event through event manager"""
        # Arrange
        event_manager = EventManager()

        # Act
        quit_event = QuitEvent()
        event_manager.post(quit_event)

        # Assert
        mock_pygame_quit.assert_not_called()

    @mock.patch("src.engine.view.PygameView.render")
    def test_notify_render(self, mock_render):
        """Test the notify function by posting an event through event manager"""
        # Arrange
        event_manager = EventManager()
        model = GameEngine(event_manager)
        pygame_instance = PygameView(event_manager, model)

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
        pygame_instance = PygameView(event_manager, model)

        # Act
        load_images = pygame_instance.load_images()

        # Assert
        expected_result = None
        assert load_images != expected_result

    @mock.patch(
        "src.engine.view.PygameView.initialise", mock.MagicMock(return_value=False)
    )
    def test_render_when_not_initialised(self):
        """Test that render is not called when pygame has not been initialised"""
        # Arrange
        event_manager = EventManager()
        model = GameEngine(event_manager)
        pygame_instance = PygameView(event_manager, model)

        # Act
        # Act is patched out

        # Assert
        assert pygame_instance.render() is None

    @mock.patch("src.engine.view.pygame.display.flip")
    @mock.patch("src.engine.view.PygameView.draw_files_and_rank")
    @mock.patch("src.engine.view.PygameView.draw_pieces")
    @mock.patch("src.engine.view.PygameView.draw_board")
    def test_render_when_initialised(
        self, mock_draw_board, mock_draw_piece, mock_draw_raf, mock_pygame_display_flip
    ):
        """Test that render is called when view has been initialised"""
        # Arrange
        event_manager = EventManager()
        model = GameEngine(event_manager)
        pygame_instance = PygameView(event_manager, model)

        tick_event = TickEvent()
        event_manager.post(tick_event)

        # Assert
        mock_draw_piece.assert_called()
        mock_draw_board.assert_called()
        mock_draw_raf.assert_called()
        mock_pygame_display_flip.assert_called()

    @mock.patch("src.engine.view.pygame.draw.rect")
    def test_draw_board(self, mock_draw_rect):
        """Test that render is called when view has been initialised"""
        # Arrange
        event_manager = EventManager()
        model = GameEngine(event_manager)
        pygame_instance = PygameView(event_manager, model)

        pygame_instance.draw_board()

        # Assert
        assert mock_draw_rect.call_count == 64
