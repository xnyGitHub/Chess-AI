"""Test class for src/engine/event_manager.py"""  # pylint: disable=too-few-public-methods
from unittest.mock import Mock, patch
from src.engine.event_manager import (
    EventManager,
    Event,
    QuitEvent,
    ClickEvent,
    TickEvent,
)


class DummyRegisteredListener:
    """Dummy Listener that CAN registered in the event_manager"""

    def __init__(self, ev_manager):
        """Init method for fake event manager"""
        self.ev_manager = ev_manager
        ev_manager.register_listener(self)

    def unregister(self):
        """Unregister the controller from the set of listeners"""
        self.ev_manager.unregister_listener(self)

    def notify(self):
        """Notify listener of event"""
        return "Notified!"


class DummyUnregisteredListener:
    """Dummy Listener that CANT registered in the event_manager"""

    def __init__(self, ev_manager):
        """Init method for fake event manager"""
        self.ev_manager = ev_manager

    def notify(self):
        """Notify listener of event"""
        return "Notified!"


class TestEvents:
    """Test the event types, QuitEvent, TickEvent etc."""

    def test_event(self):
        """Test the generic event"""
        new_event = Event()
        assert str(new_event) == "Generic event"

    def test_quit_event(self):
        """Test the quit event"""
        new_quit_event = QuitEvent()
        assert str(new_quit_event) == "Quit event"
        assert isinstance(new_quit_event, Event)

    def test_click_event(self):
        """Test the click event"""
        click_location = (45, 45)
        new_click_event = ClickEvent(click_location)
        assert str(new_click_event) == "Click event"
        assert isinstance(new_click_event, Event)

    def test_tick_event(self):
        """Test the tick event"""
        new_tick_event = TickEvent()
        assert str(new_tick_event) == "Tick event"
        assert isinstance(new_tick_event, Event)


class TestEventManager:
    """Test the functionality of the event manager"""

    def test_event_manager_listerners(self):
        """Test whether register_listener and unregister_listener work"""
        event_manager = EventManager()
        dummy_registred_listener = DummyRegisteredListener(event_manager)

        dummy_unregistred_listener = DummyUnregisteredListener(event_manager)

        assert dummy_registred_listener in event_manager.listeners
        assert dummy_unregistred_listener not in event_manager.listeners

        dummy_registred_listener.unregister()

        assert dummy_registred_listener not in event_manager.listeners

    @patch.object(DummyUnregisteredListener, "notify")
    @patch.object(DummyRegisteredListener, "notify")
    def test_listener_notify(self, mock_registered_notify, mock_unregistered_notify):
        """Tests that registered listeners get notified and unregistered listeners dont"""
        event_manager = EventManager()
        dummy_registred_listener = DummyRegisteredListener(event_manager)
        dummy_unregistred_listener = DummyUnregisteredListener(event_manager)

        fake_event_type = Mock()
        event_manager.post(fake_event_type)

        mock_registered_notify.assert_called_with(fake_event_type)
        mock_unregistered_notify.assert_not_called()

        dummy_registred_listener.unregister()

        event_manager.post(fake_event_type)
        assert mock_registered_notify.call_count == 1
