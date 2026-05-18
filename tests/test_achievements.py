"""Tests for achievement definitions and unlock checks."""

import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock

for module in ["pynput", "pynput.keyboard", "pynput.mouse"]:
    try:
        __import__(module)
    except ImportError:
        sys.modules[module] = MagicMock()

from bongo_cat.models.achievements import AchievementManager


class TestAchievementDefinitions(unittest.TestCase):
    """Achievement definitions should stay complete and ordered."""

    def _manager(self):
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        save_path = os.path.join(temp_dir.name, "achievements.json")
        return AchievementManager(save_path=save_path)

    def test_achievement_ids_are_unique(self):
        manager = self._manager()
        achievement_ids = [achievement.id for achievement in manager.get_all_achievements()]

        self.assertEqual(len(achievement_ids), len(set(achievement_ids)))

    def test_total_achievement_count(self):
        manager = self._manager()

        self.assertEqual(70, len(manager.get_all_achievements()))

    def test_slap_milestones_are_sorted(self):
        manager = self._manager()
        slap_requirements = [
            achievement.requirement
            for achievement in manager.get_all_achievements()
            if achievement.category == "slaps"
        ]

        self.assertEqual(sorted(slap_requirements), slap_requirements)

    def test_science_and_constant_slap_milestones_unlock(self):
        manager = self._manager()
        expected_ids = {
            "slaps_7",
            "slaps_8",
            "slaps_12",
            "slaps_32",
            "slaps_42",
            "slaps_46",
            "slaps_99",
            "slaps_128",
            "slaps_206",
            "slaps_212",
            "slaps_314",
            "slaps_366",
            "slaps_460",
            "slaps_767",
            "slaps_1024",
            "slaps_1618",
            "slaps_1760",
            "slaps_3220",
            "slaps_3959",
            "slaps_5280",
            "slaps_6022",
            "slaps_6371",
            "slaps_7917",
            "slaps_8760",
            "slaps_10080",
            "slaps_14700",
            "slaps_24901",
            "slaps_27182",
            "slaps_31415",
            "slaps_32768",
            "slaps_65536",
            "slaps_86400",
            "slaps_186282",
            "slaps_238855",
            "slaps_384400",
            "slaps_524288",
            "slaps_1000000",
            "slaps_1048576",
            "slaps_1618034",
            "slaps_2718282",
            "slaps_3141593",
            "slaps_5280000",
            "slaps_5865696",
            "slaps_10000000",
        }

        unlocked = manager.check_slap_count(10000000)

        self.assertTrue(expected_ids.issubset({achievement.id for achievement in unlocked}))


if __name__ == "__main__":
    unittest.main()
