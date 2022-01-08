"""Test class for src/engine/controller.py"""  # pylint: disable=attribute-defined-outside-init
import random
from unittest import mock
from unittest.mock import Mock, patch, create_autospec
from src.engine.controller import Controller
from src.engine.event_manager import EventManager, TickEvent


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


class TestControllerClickEvents:
    """Class for testing whether click events are regsitered"""

    def setup_method(self):
        """Setup method that mocks out pygame initialisation"""
        patched = mock.patch("src.engine.controller.pygame")
        self.mock_pygame = patched.start()

        patched = mock.patch("src.engine.event_manager.EventManager")
        self.mock_event_manager = patched.start()

        patched = mock.patch("src.engine.model.GameEngine")
        self.mock_game_engine = patched.start()

        self.controller = Controller(self.mock_event_manager, self.mock_game_engine)

        self.pyevent_response_mock_1 = Mock()
        self.pyevent_response_mock_1.type = self.mock_pygame.MOUSEBUTTONDOWN
        self.mock_pygame.event.get.return_value = [self.pyevent_response_mock_1]

        self.x_cord = None
        self.y_cord = None
        print("TestControllerClickEvents Setup running...")

    def teardown_method(self):
        """Tear down method that stops the mocks"""
        print("Teardown running...")
        mock.patch.stopall()

    def generate_valid_click_cords(self):
        """Generate a random valid click"""
        self.x_cord = random.randint(1, 511)
        self.y_cord = random.randint(1, 511)
        self.mock_pygame.mouse.get_pos.return_value = (self.x_cord, self.y_cord)

    def generate_same_click_cords(self):
        """Generate a deterministic click"""
        self.x_cord = 100
        self.y_cord = 100
        self.mock_pygame.mouse.get_pos.return_value = (self.x_cord, self.y_cord)

    def test_two_valid_click_events(self):
        """Unit test click_event for model.py"""

        self.generate_valid_click_cords()
        click_one = int(self.x_cord / 64), int(self.y_cord / 64)

        new_tick_event = TickEvent()
        self.controller.notify(new_tick_event)

        assert self.controller.square_selected == click_one
        assert self.controller.player_clicks == [click_one]
        assert not self.controller.most_recent_valid_move_click

        self.generate_valid_click_cords()
        click_two = int(self.x_cord / 64), int(self.y_cord / 64)

        self.controller.notify(new_tick_event)

        assert not self.controller.square_selected
        assert not self.controller.player_clicks
        assert self.controller.most_recent_valid_move_click == [click_one, click_two]

    def test_two_valid_same_cord_click_events(self):
        """Unit test click_event for model.py"""
        self.generate_same_click_cords()
        click_one = int(self.x_cord / 64), int(self.y_cord / 64)

        new_tick_event = TickEvent()
        self.controller.notify(new_tick_event)

        assert self.controller.square_selected == click_one
        assert self.controller.player_clicks == [click_one]
        assert not self.controller.most_recent_valid_move_click

        self.generate_same_click_cords()

        new_tick_event = TickEvent()
        self.controller.notify(new_tick_event)

        assert not self.controller.square_selected
        assert not self.controller.player_clicks
        assert not self.controller.most_recent_valid_move_click
