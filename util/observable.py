from typing import List
from util.observer import Observer


class Observable(object):
    """An inplementation of the observable class in the observer design
    pattern.

    === Private Attributes ===
        _observers:
            The list of observers observing this object.
    """
    _observers: List[Observer]

    def __init__(self):
        """Create a new Observable object."""
        self._observers = []

    def notify_observers(self):
        """Runs when the observed object notifies its observers."""
        for observer in self._observers:
            observer.on_notify()

    def add_observer(self, observer: Observer):
        """Add an observer to the collection."""
        self._observers.append(observer)

    def remove_observer(self, observer: Observer):
        """Remove an observer from the collection."""
        self._observers.remove(observer)

    def clear_observers(self):
        """Remove all observers from the collection."""
        self._observers.clear()
