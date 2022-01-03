"""Test class for src/engine/controller.py"""
import random
from unittest.mock import Mock, patch, create_autospec
from src.engine.controller import Controller
from src.engine.event_manager import EventManager, TickEvent
from src.engine.model import GameEngine


class TestControllerMain:
    """Test class for testing __init__"""

    @patch("src.engine.event_manager.EventManager")
    @patch("src.engine.model.GameEngine")
    def test_controller_registered_as_listener(
        self, mock_game_engine, mock_event_manager
    ):
        """Test that the controller register itself as a listner"""
        # Arrange
        mock_game_engine = mock_game_engine(mock_event_manager)
        controller = Controller(mock_event_manager, mock_game_engine)

        # Act
        mock_event_manager.register_listener.assert_called_once_with(controller)

        # Assert
        assert controller.model == mock_game_engine

    @patch("src.engine.model.GameEngine")
    def test_controller_unregister(self, mock_game_engine):
        """Test that the controller unregisters itself as a listner"""
        # Arrange
        event_manager = EventManager()
        mock_game_engine = mock_game_engine(event_manager)
        controller = Controller(event_manager, mock_game_engine)

        # Assert
        assert controller in event_manager.listeners

        # Act
        controller.unregister()

        # Assert
        assert controller not in event_manager.listeners


class TestControllerNotify:
    """Test class for testing controller.notify"""

    @patch("src.engine.controller.QuitEvent")
    @patch("src.engine.controller.pygame")
    @patch("src.engine.model.GameEngine")
    def test_controller_notify_pygame_quit(
        self, mock_engine, mock_pygame, mock_quit_event
    ):
        """
        Test that a QuitEvent is posted when pygame.QUIT event
        is inserted into the pygame event queue
        """
        # Arrange
        mock_event_manager = create_autospec(EventManager)
        mock_game_engine = mock_engine(mock_event_manager)
        controller = Controller(mock_event_manager, mock_game_engine)

        pyevent_response_mock_1 = Mock()
        pyevent_response_mock_1.type = mock_pygame.QUIT

        mock_pygame.event.get.return_value = [pyevent_response_mock_1]

        # Act
        new_tick_event = TickEvent()
        controller.notify(new_tick_event)

        # Assert
        mock_event_manager.post.assert_called_once_with(mock_quit_event())

    @patch("src.engine.controller.Event")
    @patch("src.engine.controller.pygame")
    @patch("src.engine.model.GameEngine")
    def test_controller_notify_pygame_keydown(
        self, mock_engine, mock_pygame, mock_base_event
    ):
        """
        Test that a QuitEvent is posted when pygame.QUIT event
        is inserted into the pygame event queue
        """
        # Arrange
        mock_event_manager = create_autospec(EventManager)
        mock_game_engine = mock_engine(mock_event_manager)
        controller = Controller(mock_event_manager, mock_game_engine)

        pyevent_response_mock_1 = Mock()
        pyevent_response_mock_1.type = mock_pygame.KEYDOWN

        mock_pygame.event.get.return_value = [pyevent_response_mock_1]

        # Act
        new_tick_event = TickEvent()
        controller.notify(new_tick_event)

        # Assert
        mock_event_manager.post.assert_called_once_with(mock_base_event())

    @patch("src.engine.controller.pygame")
    def test_controller_notify_pygame_mousebutton(self, mock_pygame):
        """
        Test that a QuitEvent is posted when pygame.QUIT event
        is inserted into the pygame event queue
        """
        # Arrange
        event_manager = EventManager()
        game_engine = GameEngine(event_manager)
        controller = Controller(event_manager, game_engine)

        pyevent_response_mock_1 = Mock()
        pyevent_response_mock_1.type = mock_pygame.MOUSEBUTTONDOWN

        mock_pygame.event.get.return_value = [pyevent_response_mock_1]

        x_cord = random.randint(1, 511)
        y_cord = random.randint(1, 511)
        mock_pygame.mouse.get_pos.return_value = (x_cord, y_cord)

        col = int(x_cord / 64)
        row = int(y_cord / 64)

        # Act
        new_tick_event = TickEvent()
        controller.notify(new_tick_event)

        # Assert
        assert game_engine.square_selected == (col, row)
