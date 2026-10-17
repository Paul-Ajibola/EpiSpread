"""Game settings: grid dimensions, infection rates, action points."""

from dataclasses import dataclass


@dataclass
class Settings:
    grid_width: int = 20
    grid_height: int = 20
    initial_infections: int = 3
    infection_rate: float = 0.15
    recovery_rate: float = 0.10
    mortality_rate: float = 0.05
    action_points_per_turn: int = 5
    win_turns_clean: int = 5
    population_loss_threshold: int = 200