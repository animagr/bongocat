"""Coordinated input management for all input sources."""

import logging
from typing import Callable

from .keyboard_listener import KeyboardListener
from .mouse_listener import MouseListener

logger = logging.getLogger("BongoCat")


class InputManager:
    """Manages all input listeners (keyboard, mouse).

    Coordinates multiple input sources and provides unified start/stop control.

    Attributes:
        callback: Function to call when any input is detected
        keyboard_listener: Keyboard input listener
        mouse_listener: Mouse input listener
    """

    def __init__(self, callback: Callable[[], None]):
        """Initialize input manager with all listeners.

        Args:
            callback: Function to call when any input is detected
        """
        self.callback = callback

        self.keyboard_listener = KeyboardListener(callback)
        self.mouse_listener = MouseListener(callback)

        logger.info("Input manager initialized")

    def start(self) -> None:
        """Start all input listeners."""
        logger.info("Starting all input listeners...")

        self.keyboard_listener.start()
        self.mouse_listener.start()

        logger.info("All input listeners started")

    def stop(self) -> None:
        """Stop all input listeners."""
        logger.info("Stopping all input listeners...")

        self.keyboard_listener.stop()
        self.mouse_listener.stop()

        logger.info("All input listeners stopped")

    def is_running(self) -> bool:
        """Check if any listener is currently running.

        Returns:
            True if at least one listener is active, False otherwise
        """
        return (
            self.keyboard_listener.is_running() or
            self.mouse_listener.is_running()
        )

    def get_status(self) -> dict:
        """Get status of all listeners.

        Returns:
            Dictionary with status of each listener

        Example:
            >>> manager.get_status()
            {'keyboard': True, 'mouse': True}
        """
        return {
            'keyboard': self.keyboard_listener.is_running(),
            'mouse': self.mouse_listener.is_running(),
        }
