"""Daily plant companion state for Bongo Cat."""

import json
import logging
import os
import random
from dataclasses import dataclass
from datetime import date
from typing import Callable, Dict, List, Optional, Tuple

from ..utils import resource_path

logger = logging.getLogger("BongoCat")


@dataclass(frozen=True)
class PlantStage:
    """A plant stage unlocked at a slap-point threshold."""

    name: str
    threshold: int
    image: str


class PlantManager:
    """Manages the slap-grown daily sunflower companion.

    Plant progress intentionally resets each calendar day. The manager does not
    use the lifetime BongoCat slap count; it keeps a separate daily counter in
    ``plant_state.json``.
    """

    STAGES: List[PlantStage] = [
        PlantStage("seed", 0, "seed.png"),
        PlantStage("seedling", 1000, "seedling.png"),
        PlantStage("growing1", 2500, "growing1.png"),
        PlantStage("young", 5000, "young.png"),
        PlantStage("growing2", 8000, "growing2.png"),
        PlantStage("growing3", 12500, "growing3.png"),
        PlantStage("mature", 16000, "mature.png"),
        PlantStage("flowering", 20000, "flowering.png"),
        PlantStage("seed-bearing", 25000, "seed-bearing.png"),
    ]

    SPECIES = "sunflower"
    USE_RANDOM_SPECIES = False

    def __init__(
        self,
        save_path: Optional[str] = None,
        date_provider: Callable[[], date] = date.today,
    ):
        self.save_path = save_path or resource_path("plant_state.json")
        self.date_provider = date_provider
        self.state = self._load_state()
        self._reset_if_new_day()

    @property
    def today_key(self) -> str:
        """Return today's ISO date."""
        return self.date_provider().isoformat()

    @property
    def today_points(self) -> int:
        """Return today's separate plant slap points."""
        return int(self.state.get("today_points", 0))

    @property
    def stage(self) -> str:
        """Return the current plant stage."""
        return str(self.state.get("stage", "seed"))

    @property
    def species(self) -> str:
        """Return the current plant species for today's display."""
        if not self.USE_RANDOM_SPECIES:
            return self.SPECIES
        return str(self.state.get("species", self.SPECIES))

    def record_slap(self, count: int = 1) -> bool:
        """Add slap points to today's plant and return whether stage changed."""
        self._reset_if_new_day()
        previous_stage = self.stage
        next_points = max(0, self.today_points + max(0, count))
        next_stage = self.stage_for_points(next_points)

        self.state["today_points"] = next_points
        if next_stage != previous_stage:
            self.state["last_stage"] = previous_stage
            self.state["stage"] = next_stage
            logger.info(
                f"Plant grew "
                f"at {next_points:,} daily slaps"
            )
        else:
            self.state["stage"] = previous_stage

        self.save()
        return next_stage != previous_stage

    def save(self) -> None:
        """Persist plant progress to disk."""
        try:
            save_dir = os.path.dirname(self.save_path)
            if save_dir:
                os.makedirs(save_dir, exist_ok=True)
            with open(self.save_path, "w", encoding="utf-8") as f:
                json.dump(self.state, f, indent=2)
        except (IOError, OSError) as e:
            logger.error(f"Error saving plant state to {self.save_path}: {e}")

    def image_path_for_stage(self, stage: Optional[str] = None) -> str:
        """Return the relative resource path for a stage image."""
        stage_name = stage or self.stage
        image = self._stage_images().get(stage_name, "seed.png")
        return os.path.join("plant", self.species, image)

    def sparkle_image_path(self) -> str:
        """Return the relative resource path for the sparkle overlay image."""
        return os.path.join("plant", self.species, "sparkle.png")

    @classmethod
    def stage_for_points(cls, points: int) -> str:
        """Return the highest unlocked stage for a point total."""
        stage_name = cls.STAGES[0].name
        safe_points = max(0, int(points))
        for stage in cls.STAGES:
            if safe_points >= stage.threshold:
                stage_name = stage.name
            else:
                break
        return stage_name

    @classmethod
    def thresholds(cls) -> List[Tuple[str, int]]:
        """Return stage thresholds as ``(name, threshold)`` tuples."""
        return [(stage.name, stage.threshold) for stage in cls.STAGES]

    @classmethod
    def _stage_images(cls) -> Dict[str, str]:
        return {stage.name: stage.image for stage in cls.STAGES}

    def _load_state(self) -> Dict[str, object]:
        if not os.path.exists(self.save_path):
            return self._default_state()

        try:
            with open(self.save_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
        except (json.JSONDecodeError, IOError, OSError):
            return self._default_state()

        if not isinstance(loaded, dict):
            return self._default_state()

        points = self._coerce_points(loaded.get("today_points", 0))
        stage = self.stage_for_points(points)
        species = loaded.get("species")
        if not isinstance(species, str) or not species:
            species = self._default_species()

        return {
            "date": str(loaded.get("date", self.today_key)),
            "today_points": points,
            "stage": stage,
            "last_stage": str(loaded.get("last_stage", stage)),
            "species": species,
        }

    def _reset_if_new_day(self) -> None:
        if self.state.get("date") == self.today_key:
            return
        self.state = self._default_state()
        self.save()

    def _default_state(self) -> Dict[str, object]:
        return {
            "date": self.today_key,
            "today_points": 0,
            "stage": "seed",
            "last_stage": "seed",
            "species": self._default_species(),
        }

    @classmethod
    def _available_species(cls) -> List[str]:
        plant_root = resource_path("plant")
        try:
            return sorted(
                entry.name
                for entry in os.scandir(plant_root)
                if entry.is_dir()
            )
        except (FileNotFoundError, OSError):
            return []

    @classmethod
    def _random_species(cls) -> str:
        species = cls._available_species()
        return random.choice(species) if species else cls.SPECIES

    @classmethod
    def _default_species(cls) -> str:
        if not cls.USE_RANDOM_SPECIES:
            return cls.SPECIES
        return cls._random_species()

    @staticmethod
    def _coerce_points(value: object) -> int:
        try:
            return max(0, int(value))
        except (TypeError, ValueError):
            return 0
