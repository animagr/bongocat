"""Achievement system for Bongo Cat."""

import json
import os
import logging
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, asdict
from datetime import datetime

logger = logging.getLogger("BongoCat")


@dataclass
class Achievement:
    """An achievement definition.

    Attributes:
        id: Unique identifier for the achievement
        name: Display name of the achievement
        description: Description of how to unlock
        icon: Icon emoji or character
        category: Category (slaps, combos, time, special)
        hidden: Whether the achievement is hidden until unlocked
        requirement: Requirement value (e.g., slap count)
        unlocked: Whether the achievement is unlocked
        unlock_time: When the achievement was unlocked (ISO format)
    """
    id: str
    name: str
    description: str
    icon: str
    category: str
    hidden: bool = False
    requirement: int = 0
    unlocked: bool = False
    unlock_time: Optional[str] = None


class AchievementManager:
    """Manages achievement tracking and unlocking.

    Achievements are saved to achievements.json in the user's config directory.

    Attributes:
        achievements: Dictionary of all achievements
        unlocked_count: Number of unlocked achievements
        save_path: Path to save file
        on_unlock_callback: Callback function when achievement unlocks
    """

    def __init__(self, save_path: str = "achievements.json"):
        """Initialize the achievement manager.

        Args:
            save_path: Path to save unlocked achievements
        """
        self.achievements: Dict[str, Achievement] = {}
        self.unlocked_count = 0
        self.save_path = save_path
        self.on_unlock_callback: Optional[Callable[[Achievement], None]] = None

        self._define_achievements()
        self._load_progress()

    def _define_achievements(self) -> None:
        """Define all available achievements."""
        achievement_defs = [
            # Slap Count Achievements
            Achievement(
                id="first_slap",
                name="First Slap!",
                description="Perform your first slap",
                icon="👋",
                category="slaps",
                requirement=1
            ),
            Achievement(
                id="slaps_7",
                name="Neutral Zone",
                description="Reach 7 slaps, the neutral pH of pure water",
                icon="💧",
                category="slaps",
                requirement=7
            ),
            Achievement(
                id="slaps_8",
                name="Byte Sized",
                description="Reach 8 slaps, one for every bit in a byte",
                icon="💾",
                category="slaps",
                requirement=8
            ),
            Achievement(
                id="slaps_12",
                name="Footwork",
                description="Reach 12 slaps, one for every inch in a foot",
                icon="📏",
                category="slaps",
                requirement=12
            ),
            Achievement(
                id="slaps_32",
                name="Freezing Point",
                description="Reach 32 slaps, the freezing point of water in Fahrenheit",
                icon="🧊",
                category="slaps",
                requirement=32
            ),
            Achievement(
                id="slaps_42",
                name="Answer to Everything",
                description="Reach 42 slaps",
                icon="✨",
                category="slaps",
                requirement=42
            ),
            Achievement(
                id="slaps_46",
                name="Chromosome Chorus",
                description="Reach 46 slaps, one for every chromosome in a human cell",
                icon="🧬",
                category="slaps",
                requirement=46
            ),
            Achievement(
                id="slaps_99",
                name="Body Heat",
                description="Reach 99 slaps, roughly normal body temperature in Fahrenheit",
                icon="🌡️",
                category="slaps",
                requirement=99
            ),
            Achievement(
                id="slaps_100",
                name="Century Club",
                description="Reach 100 slaps",
                icon="💯",
                category="slaps",
                requirement=100
            ),
            Achievement(
                id="slaps_128",
                name="IPv6 Initiate",
                description="Reach 128 slaps, one for every bit in an IPv6 address",
                icon="🌐",
                category="slaps",
                requirement=128
            ),
            Achievement(
                id="slaps_206",
                name="Bone Rhythm",
                description="Reach 206 slaps, one for every bone in an adult human body",
                icon="🦴",
                category="slaps",
                requirement=206
            ),
            Achievement(
                id="slaps_212",
                name="Boiling Point",
                description="Reach 212 slaps, the boiling point of water in Fahrenheit",
                icon="♨️",
                category="slaps",
                requirement=212
            ),
            Achievement(
                id="slaps_314",
                name="Pi Paws",
                description="Reach 314 slaps, pi times one hundred",
                icon="🥧",
                category="slaps",
                requirement=314
            ),
            Achievement(
                id="slaps_366",
                name="Leap Year",
                description="Reach 366 slaps, one for every day in a leap year",
                icon="📆",
                category="slaps",
                requirement=366
            ),
            Achievement(
                id="slaps_460",
                name="Absolute Zero",
                description="Reach 460 slaps, absolute zero rounded in Fahrenheit",
                icon="❄️",
                category="slaps",
                requirement=460
            ),
            Achievement(
                id="slaps_500",
                name="Dedicated Drummer",
                description="Reach 500 slaps",
                icon="🥁",
                category="slaps",
                requirement=500
            ),
            Achievement(
                id="slaps_767",
                name="Sound Barrier Warmup",
                description="Reach 767 slaps, the speed of sound in mph at sea level",
                icon="🔊",
                category="slaps",
                requirement=767
            ),
            Achievement(
                id="slaps_1000",
                name="Thousand Taps",
                description="Reach 1,000 slaps",
                icon="🎯",
                category="slaps",
                requirement=1000
            ),
            Achievement(
                id="slaps_1024",
                name="Kilobyte Club",
                description="Reach 1,024 slaps, one for every byte in a kibibyte",
                icon="🧮",
                category="slaps",
                requirement=1024
            ),
            Achievement(
                id="slaps_1618",
                name="Golden Paws",
                description="Reach 1,618 slaps, the golden ratio times one thousand",
                icon="φ",
                category="slaps",
                requirement=1618
            ),
            Achievement(
                id="slaps_1760",
                name="Yard Mile",
                description="Reach 1,760 slaps, one for every yard in a mile",
                icon="🛣️",
                category="slaps",
                requirement=1760
            ),
            Achievement(
                id="slaps_3220",
                name="Gravity Assist",
                description="Reach 3,220 slaps, gravity in ft/s² times one hundred",
                icon="🪐",
                category="slaps",
                requirement=3220
            ),
            Achievement(
                id="slaps_3959",
                name="Earth Core Tap",
                description="Reach 3,959 slaps, Earth's average radius in miles",
                icon="🌎",
                category="slaps",
                requirement=3959
            ),
            Achievement(
                id="slaps_5000",
                name="Rhythm Master",
                description="Reach 5,000 slaps",
                icon="🎵",
                category="slaps",
                requirement=5000
            ),
            Achievement(
                id="slaps_5280",
                name="Mile Marker",
                description="Reach 5,280 slaps, one for every foot in a mile",
                icon="🏁",
                category="slaps",
                requirement=5280
            ),
            Achievement(
                id="slaps_6022",
                name="Avogadro Appetizer",
                description="Reach 6,022 slaps, Avogadro's mantissa times one thousand",
                icon="⚗️",
                category="slaps",
                requirement=6022
            ),
            Achievement(
                id="slaps_6371",
                name="Metric Earth Core",
                description="Reach 6,371 slaps, Earth's average radius in kilometers",
                icon="🧭",
                category="slaps",
                requirement=6371
            ),
            Achievement(
                id="slaps_7917",
                name="Blue Marble",
                description="Reach 7,917 slaps, Earth's average diameter in miles",
                icon="🌏",
                category="slaps",
                requirement=7917
            ),
            Achievement(
                id="slaps_8760",
                name="Year of Hours",
                description="Reach 8,760 slaps, one for every hour in a year",
                icon="⌛",
                category="slaps",
                requirement=8760
            ),
            Achievement(
                id="slaps_10000",
                name="Ten Thousand Touches",
                description="Reach 10,000 slaps",
                icon="⭐",
                category="slaps",
                requirement=10000
            ),
            Achievement(
                id="slaps_10080",
                name="Week of Minutes",
                description="Reach 10,080 slaps, one for every minute in a week",
                icon="🗓️",
                category="slaps",
                requirement=10080
            ),
            Achievement(
                id="slaps_14700",
                name="Sea Level Standard",
                description="Reach 14,700 slaps, atmospheric pressure in psi times one thousand",
                icon="🌊",
                category="slaps",
                requirement=14700
            ),
            Achievement(
                id="slaps_24901",
                name="Earth Lap",
                description="Reach 24,901 slaps, Earth's equatorial circumference in miles",
                icon="🌍",
                category="slaps",
                requirement=24901
            ),
            Achievement(
                id="slaps_25000",
                name="Quarter Century",
                description="Reach 25,000 slaps",
                icon="🎖️",
                category="slaps",
                requirement=25000
            ),
            Achievement(
                id="slaps_27182",
                name="Euler Energy",
                description="Reach 27,182 slaps, Euler's number times ten thousand",
                icon="ℯ",
                category="slaps",
                requirement=27182
            ),
            Achievement(
                id="slaps_31415",
                name="Five-Digit Pi",
                description="Reach 31,415 slaps, pi times ten thousand",
                icon="π",
                category="slaps",
                requirement=31415
            ),
            Achievement(
                id="slaps_32768",
                name="Signed Short Stack",
                description="Reach 32,768 slaps, 2 to the 15th power",
                icon="🧱",
                category="slaps",
                requirement=32768
            ),
            Achievement(
                id="slaps_50000",
                name="Fifty Thousand Fury",
                description="Reach 50,000 slaps",
                icon="👑",
                category="slaps",
                requirement=50000
            ),
            Achievement(
                id="slaps_65536",
                name="Sixteen-Bit Summit",
                description="Reach 65,536 slaps, 2 to the 16th power",
                icon="💿",
                category="slaps",
                requirement=65536
            ),
            Achievement(
                id="slaps_86400",
                name="Full Day Cycle",
                description="Reach 86,400 slaps, one for every second in a day",
                icon="🕛",
                category="slaps",
                requirement=86400
            ),
            Achievement(
                id="slaps_100000",
                name="One Hundred Thousand Legend",
                description="Reach 100,000 slaps",
                icon="🏆",
                category="slaps",
                requirement=100000
            ),
            Achievement(
                id="slaps_186282",
                name="Light Speed Snapshot",
                description="Reach 186,282 slaps, the speed of light in miles per second",
                icon="💡",
                category="slaps",
                requirement=186282
            ),
            Achievement(
                id="slaps_238855",
                name="Moonshot",
                description="Reach 238,855 slaps, the average distance to the Moon in miles",
                icon="🌕",
                category="slaps",
                requirement=238855
            ),
            Achievement(
                id="slaps_384400",
                name="Metric Moonshot",
                description="Reach 384,400 slaps, the average distance to the Moon in kilometers",
                icon="🚀",
                category="slaps",
                requirement=384400
            ),
            Achievement(
                id="slaps_524288",
                name="Nineteen-Bit Beat",
                description="Reach 524,288 slaps, 2 to the 19th power",
                icon="🖥️",
                category="slaps",
                requirement=524288
            ),
            Achievement(
                id="slaps_1000000",
                name="Megaslap",
                description="Reach 1,000,000 slaps",
                icon="🔬",
                category="slaps",
                requirement=1000000
            ),
            Achievement(
                id="slaps_1048576",
                name="True Megabyte",
                description="Reach 1,048,576 slaps, 2 to the 20th power",
                icon="💽",
                category="slaps",
                requirement=1048576
            ),
            Achievement(
                id="slaps_1618034",
                name="Golden Million",
                description="Reach 1,618,034 slaps, the golden ratio scaled to a million",
                icon="🏛️",
                category="slaps",
                requirement=1618034
            ),
            Achievement(
                id="slaps_2718282",
                name="Euler Engine",
                description="Reach 2,718,282 slaps, Euler's number scaled to a million",
                icon="📈",
                category="slaps",
                requirement=2718282
            ),
            Achievement(
                id="slaps_3141593",
                name="Pi Millionaire",
                description="Reach 3,141,593 slaps, pi scaled to a million",
                icon="🥧",
                category="slaps",
                requirement=3141593
            ),
            Achievement(
                id="slaps_5280000",
                name="Thousand-Mile March",
                description="Reach 5,280,000 slaps, one for every foot in 1,000 miles",
                icon="🗺️",
                category="slaps",
                requirement=5280000
            ),
            Achievement(
                id="slaps_5865696",
                name="Light Second",
                description="Reach 5,865,696 slaps, the distance light travels in one second in feet",
                icon="🌌",
                category="slaps",
                requirement=5865696
            ),
            Achievement(
                id="slaps_10000000",
                name="Ten Megaslaps",
                description="Reach 10,000,000 slaps",
                icon="🧠",
                category="slaps",
                requirement=10000000
            ),

            # Combo Achievements
            Achievement(
                id="combo_10",
                name="Getting Started",
                description="Achieve a 10x combo",
                icon="🔟",
                category="combos",
                requirement=10
            ),
            Achievement(
                id="combo_25",
                name="Combo Novice",
                description="Achieve a 25x combo",
                icon="🔥",
                category="combos",
                requirement=25
            ),
            Achievement(
                id="combo_50",
                name="Combo Expert",
                description="Achieve a 50x combo",
                icon="⚡",
                category="combos",
                requirement=50
            ),
            Achievement(
                id="combo_100",
                name="Combo Master",
                description="Achieve a 100x combo",
                icon="💥",
                category="combos",
                requirement=100
            ),
            Achievement(
                id="combo_200",
                name="Unstoppable",
                description="Achieve a 200x combo",
                icon="🌟",
                category="combos",
                requirement=200
            ),
            Achievement(
                id="combo_300",
                name="Triple Century",
                description="Achieve a 300x combo",
                icon="🚀",
                category="combos",
                requirement=300
            ),
            Achievement(
                id="combo_500",
                name="Five Hundred Frenzy",
                description="Achieve a 500x combo",
                icon="🔮",
                category="combos",
                requirement=500
            ),
            Achievement(
                id="combo_1000",
                name="Legendary Combo",
                description="Achieve a 1000x combo",
                icon="💎",
                category="combos",
                requirement=1000
            ),

            # Special Achievements
            Achievement(
                id="night_owl",
                name="Night Owl",
                description="Slap between midnight and 3 AM",
                icon="🦉",
                category="special",
                hidden=True
            ),
            Achievement(
                id="early_bird",
                name="Early Bird",
                description="Slap between 5 AM and 7 AM",
                icon="🐦",
                category="special",
                hidden=True
            ),
            Achievement(
                id="overload_survivor",
                name="Overload Survivor",
                description="Achieve the overload effect (60+ combo)",
                icon="💫",
                category="special",
                requirement=60
            ),
            Achievement(
                id="weekend_warrior",
                name="Weekend Warrior",
                description="Slap on Saturday or Sunday",
                icon="🎮",
                category="special",
                hidden=True
            ),
            Achievement(
                id="dedication",
                name="Dedicated",
                description="Open Bongo Cat 10 times",
                icon="📅",
                category="special",
                requirement=10
            ),
            Achievement(
                id="persistence",
                name="Persistence",
                description="Open Bongo Cat 50 times",
                icon="🎯",
                category="special",
                requirement=50
            ),
            Achievement(
                id="devotion",
                name="True Devotion",
                description="Open Bongo Cat 100 times",
                icon="💖",
                category="special",
                requirement=100
            ),
            Achievement(
                id="speed_demon",
                name="Speed Demon",
                description="Reach 10 combo in under 2 seconds",
                icon="⚡",
                category="special",
                hidden=True
            ),
            Achievement(
                id="marathon_session",
                name="Marathon Session",
                description="Keep a 100+ combo for over 30 seconds",
                icon="🏃",
                category="special",
                hidden=True
            ),
        ]

        for achievement in achievement_defs:
            self.achievements[achievement.id] = achievement

    def _load_progress(self) -> None:
        """Load achievement progress from save file."""
        if not os.path.exists(self.save_path):
            return

        try:
            with open(self.save_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for achievement_id, achievement_data in data.items():
                if achievement_id in self.achievements:
                    self.achievements[achievement_id].unlocked = achievement_data.get('unlocked', False)
                    self.achievements[achievement_id].unlock_time = achievement_data.get('unlock_time')

                    if self.achievements[achievement_id].unlocked:
                        self.unlocked_count += 1

            logger.info(f"Loaded {self.unlocked_count} unlocked achievements")

        except (json.JSONDecodeError, IOError, Exception) as e:
            logger.error(f"Error loading achievements: {e}")

    def _save_progress(self) -> None:
        """Save achievement progress to file."""
        try:
            data = {}
            for achievement_id, achievement in self.achievements.items():
                if achievement.unlocked:
                    data[achievement_id] = {
                        'unlocked': True,
                        'unlock_time': achievement.unlock_time
                    }

            with open(self.save_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)

        except (IOError, Exception) as e:
            logger.error(f"Error saving achievements: {e}")

    def unlock(self, achievement_id: str) -> bool:
        """Unlock an achievement.

        Args:
            achievement_id: ID of the achievement to unlock

        Returns:
            True if newly unlocked, False if already unlocked or not found
        """
        if achievement_id not in self.achievements:
            return False

        achievement = self.achievements[achievement_id]

        if achievement.unlocked:
            return False

        achievement.unlocked = True
        achievement.unlock_time = datetime.now().isoformat()
        self.unlocked_count += 1

        logger.info(f"🏆 Achievement Unlocked: {achievement.name}")

        self._save_progress()

        if self.on_unlock_callback:
            self.on_unlock_callback(achievement)

        return True

    def check_slap_count(self, slap_count: int) -> List[Achievement]:
        """Check and unlock slap count achievements.

        Args:
            slap_count: Current total slap count

        Returns:
            List of newly unlocked achievements
        """
        newly_unlocked = []

        for achievement in self.achievements.values():
            if achievement.category == "slaps" and not achievement.unlocked:
                if slap_count >= achievement.requirement:
                    if self.unlock(achievement.id):
                        newly_unlocked.append(achievement)

        return newly_unlocked

    def check_combo(self, combo_count: int) -> List[Achievement]:
        """Check and unlock combo achievements.

        Args:
            combo_count: Current combo count

        Returns:
            List of newly unlocked achievements
        """
        newly_unlocked = []

        for achievement in self.achievements.values():
            if achievement.category == "combos" and not achievement.unlocked:
                if combo_count >= achievement.requirement:
                    if self.unlock(achievement.id):
                        newly_unlocked.append(achievement)

        # Check overload achievement
        if combo_count >= 60 and not self.achievements["overload_survivor"].unlocked:
            if self.unlock("overload_survivor"):
                newly_unlocked.append(self.achievements["overload_survivor"])

        return newly_unlocked

    def check_time_based(self) -> List[Achievement]:
        """Check and unlock time-based achievements.

        Returns:
            List of newly unlocked achievements
        """
        newly_unlocked = []
        now = datetime.now()
        current_hour = now.hour
        current_weekday = now.weekday()  # 0 = Monday, 6 = Sunday

        # Night Owl: midnight to 3 AM
        if 0 <= current_hour < 3 and not self.achievements["night_owl"].unlocked:
            if self.unlock("night_owl"):
                newly_unlocked.append(self.achievements["night_owl"])

        # Early Bird: 5 AM to 7 AM
        if 5 <= current_hour < 7 and not self.achievements["early_bird"].unlocked:
            if self.unlock("early_bird"):
                newly_unlocked.append(self.achievements["early_bird"])

        # Weekend Warrior: Saturday (5) or Sunday (6)
        if current_weekday >= 5 and not self.achievements["weekend_warrior"].unlocked:
            if self.unlock("weekend_warrior"):
                newly_unlocked.append(self.achievements["weekend_warrior"])

        return newly_unlocked

    def check_launch_count(self, launch_count: int) -> List[Achievement]:
        """Check and unlock launch count achievements.

        Args:
            launch_count: Total number of times app has been launched

        Returns:
            List of newly unlocked achievements
        """
        newly_unlocked = []

        if launch_count >= 10 and not self.achievements["dedication"].unlocked:
            if self.unlock("dedication"):
                newly_unlocked.append(self.achievements["dedication"])

        if launch_count >= 50 and not self.achievements["persistence"].unlocked:
            if self.unlock("persistence"):
                newly_unlocked.append(self.achievements["persistence"])

        if launch_count >= 100 and not self.achievements["devotion"].unlocked:
            if self.unlock("devotion"):
                newly_unlocked.append(self.achievements["devotion"])

        return newly_unlocked

    def get_all_achievements(self) -> List[Achievement]:
        """Get all achievements.

        Returns:
            List of all achievements
        """
        return list(self.achievements.values())

    def get_unlocked_achievements(self) -> List[Achievement]:
        """Get only unlocked achievements.

        Returns:
            List of unlocked achievements
        """
        return [a for a in self.achievements.values() if a.unlocked]

    def get_progress_percent(self) -> float:
        """Get achievement completion percentage.

        Returns:
            Percentage of achievements unlocked (0-100)
        """
        if not self.achievements:
            return 0.0

        return (self.unlocked_count / len(self.achievements)) * 100

    def set_unlock_callback(self, callback: Callable[[Achievement], None]) -> None:
        """Set a callback function to be called when an achievement is unlocked.

        Args:
            callback: Function to call with the unlocked achievement
        """
        self.on_unlock_callback = callback
