"""
Event Bus - Central event distribution system
"""
from typing import Callable, Dict, List

from app.core.logging_config import get_logger
from app.events.base import BaseEvent, EventType

logger = get_logger(__name__)


class EventBus:
    """
    Event bus for publishing and subscribing to events.
    This is a simple in-memory implementation.
    For production, consider Redis Pub/Sub or message queue.
    """

    def __init__(self):
        self._subscribers: Dict[EventType, List[Callable]] = {}

    def subscribe(self, event_type: EventType, handler: Callable):
        """Subscribe a handler to an event type"""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []

        self._subscribers[event_type].append(handler)
        logger.info("event_handler_subscribed", event_type=event_type, handler=handler.__name__)

    def unsubscribe(self, event_type: EventType, handler: Callable):
        """Unsubscribe a handler from an event type"""
        if event_type in self._subscribers:
            self._subscribers[event_type].remove(handler)
            logger.info(
                "event_handler_unsubscribed", event_type=event_type, handler=handler.__name__
            )

    async def publish(self, event: BaseEvent):
        """Publish an event to all subscribers"""
        logger.info(
            "event_published",
            event_id=str(event.event_id),
            event_type=event.event_type,
            source=event.source,
        )

        handlers = self._subscribers.get(event.event_type, [])

        for handler in handlers:
            try:
                await handler(event)
            except Exception as e:
                logger.error(
                    "event_handler_failed",
                    event_id=str(event.event_id),
                    event_type=event.event_type,
                    handler=handler.__name__,
                    error=str(e),
                    exc_info=True,
                )


# Global event bus instance
event_bus = EventBus()
