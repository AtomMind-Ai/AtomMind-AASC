from collections import defaultdict
from core.logger import get_logger

logger = get_logger()

class MessageBus:
    """Lightweight in-memory pub/sub system."""
    
    def __init__(self):
        self.subscribers = defaultdict(list)

    def subscribe(self, topic, callback):
        self.subscribers[topic].append(callback)
        logger.info(f"Subscribed to {topic}")

    def publish(self, topic, message):
        logger.info(f"Message published on {topic}: {message}")
        for callback in self.subscribers.get(topic, []):
            callback(message)
