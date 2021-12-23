"""Event manager file"""


class EventManager:
    """this object is responsible for coordinating most communication
    between the Model, View, and Controller."""

    def __init__(self):
        """Constructor"""
        from weakref import WeakKeyDictionary

        self.listeners = WeakKeyDictionary()

    def register_listener(self, listener):
        """Register a listener to listen for events"""
        self.listeners[listener] = 1

    def unregister_listener(self, listener):
        """Remove a listener"""
        if listener in self.listeners.keys():
            del self.listeners[listener]

    def post(self, event):
        """Function that notifies all listers of new event"""
        for listener in self.listeners.keys():
            # NOTE: If the weakref has died, it will be
            # automatically removed, so we don't have
            # to worry about it.
            listener.notify(event)
