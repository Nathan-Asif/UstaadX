"""
WebSocket Connection Manager for real-time communication
"""
from typing import Dict, List

from fastapi import WebSocket

from app.core.logging_config import get_logger

logger = get_logger(__name__)


class ConnectionManager:
    """Manages WebSocket connections"""

    def __init__(self):
        # user_id -> list of websocket connections
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        """Accept and register a new connection"""
        await websocket.accept()

        if user_id not in self.active_connections:
            self.active_connections[user_id] = []

        self.active_connections[user_id].append(websocket)
        logger.info("websocket_connected", user_id=user_id)

    def disconnect(self, websocket: WebSocket, user_id: str):
        """Remove a connection"""
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)

            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

        logger.info("websocket_disconnected", user_id=user_id)

    async def send_personal_message(self, message: dict, user_id: str):
        """Send message to a specific user's connections"""
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(
                        "websocket_send_failed", user_id=user_id, error=str(e), exc_info=True
                    )

    async def broadcast(self, message: dict):
        """Broadcast message to all connected users"""
        for user_id, connections in self.active_connections.items():
            for connection in connections:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(
                        "websocket_broadcast_failed", user_id=user_id, error=str(e), exc_info=True
                    )


# Global connection manager instance
connection_manager = ConnectionManager()
