"""Bongo Cat Desktop Buddy - A reactive desktop pet application."""

from .models import ConfigManager, PlantManager
from .ui import BongoCatWindow, SettingsPanelWidget
from .input import InputManager
from .utils import resource_path, setup_logging
from . import animations

__version__ = "2.0.7"
__author__ = "luinbytes"
__description__ = "Interactive desktop pet that responds to keyboard and mouse inputs"

__all__ = [
    'ConfigManager',
    'PlantManager',
    'BongoCatWindow',
    'SettingsPanelWidget',
    'InputManager',
    'resource_path',
    'setup_logging',
    'animations'
]
