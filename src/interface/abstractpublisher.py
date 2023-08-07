from abc import ABC, abstractmethod

class AbstractPublisher(ABC):
    """
    An abstract interface for publishers that send messages to an external system.
    """

    @abstractmethod
    def publish(self, event):
        """
        Publishes the given event.
        :param event: The event to be published.
        """
        pass