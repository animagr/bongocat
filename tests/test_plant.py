"""Tests for daily plant companion state."""

import json
import os
import sys
import tempfile
import unittest
from datetime import date
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bongo_cat.models.plant import PlantManager


class TestPlantManager(unittest.TestCase):
    """Test plant state, thresholds, and daily reset behavior."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.state_path = os.path.join(self.temp_dir, "plant_state.json")
        self.current_date = date(2026, 5, 20)

    def tearDown(self):
        if os.path.exists(self.state_path):
            os.remove(self.state_path)
        os.rmdir(self.temp_dir)

    def make_manager(self):
        return PlantManager(
            save_path=self.state_path,
            date_provider=lambda: self.current_date,
        )

    def test_stage_thresholds(self):
        cases = [
            (0, "seed"),
            (999, "seed"),
            (1000, "seedling"),
            (2499, "seedling"),
            (2500, "growing1"),
            (5000, "young"),
            (8000, "growing2"),
            (12500, "growing3"),
            (16000, "mature"),
            (20000, "flowering"),
            (25000, "seed-bearing"),
        ]

        for points, expected_stage in cases:
            with self.subTest(points=points):
                self.assertEqual(PlantManager.stage_for_points(points), expected_stage)

    def test_record_slap_updates_separate_daily_points(self):
        manager = self.make_manager()

        self.assertFalse(manager.record_slap(999))
        self.assertEqual(manager.today_points, 999)
        self.assertEqual(manager.stage, "seed")

        self.assertTrue(manager.record_slap())
        self.assertEqual(manager.today_points, 1000)
        self.assertEqual(manager.stage, "seedling")

        with open(self.state_path, "r", encoding="utf-8") as f:
            saved = json.load(f)

        self.assertEqual(saved["date"], "2026-05-20")
        self.assertEqual(saved["today_points"], 1000)
        self.assertEqual(saved["stage"], "seedling")

    def test_new_day_resets_to_seed(self):
        manager = self.make_manager()
        manager.record_slap(5000)
        self.assertEqual(manager.stage, "young")

        self.current_date = date(2026, 5, 21)
        next_day_manager = self.make_manager()

        self.assertEqual(next_day_manager.today_points, 0)
        self.assertEqual(next_day_manager.stage, "seed")
        self.assertEqual(next_day_manager.state["date"], "2026-05-21")

    def test_missing_species_loads_random_species_for_today(self):
        with open(self.state_path, "w", encoding="utf-8") as f:
            json.dump({"date": "2026-05-20", "today_points": 0, "stage": "seed"}, f)

        with patch.object(PlantManager, "_random_species", return_value="cactus"):
            manager = self.make_manager()

        self.assertEqual(manager.species, "cactus")

    def test_species_persists_within_same_day(self):
        manager = self.make_manager()
        manager.state["species"] = "cactus"
        manager.save()

        reload_manager = self.make_manager()
        self.assertEqual(reload_manager.species, "cactus")

    def test_new_day_chooses_new_random_species(self):
        self.current_date = date(2026, 5, 20)
        with patch.object(PlantManager, "_random_species", side_effect=["sunflower", "cactus"]):
            manager = self.make_manager()
            self.assertEqual(manager.species, "sunflower")

            self.current_date = date(2026, 5, 21)
            next_day_manager = self.make_manager()

        self.assertEqual(next_day_manager.species, "cactus")

    def test_corrupt_state_falls_back_to_default(self):
        with open(self.state_path, "w", encoding="utf-8") as f:
            f.write("{not valid json")

        manager = self.make_manager()

        self.assertEqual(manager.today_points, 0)
        self.assertEqual(manager.stage, "seed")


if __name__ == '__main__':
    unittest.main()
