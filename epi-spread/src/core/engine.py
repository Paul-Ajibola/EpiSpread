"""Core simulation loop and game state machine."""

from __future__ import annotations

from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional

from src.core.grid import Grid, CellState
from src.config.settings import Settings


class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAMEOVER = auto()
    WON = auto()


@dataclass
class GameStats:
    day: int = 0
    susceptible: int = 0
    infected: int = 0
    recovered: int = 0
    dead: int = 0
    vaccinated: int = 0
    action_points: int = 0


class Engine:
    """Main simulation engine managing game state and turn progression."""

    def __init__(self, settings: Optional[Settings] = None) -> None:
        self.settings = settings or Settings()
        self.grid = Grid(self.settings.grid_width, self.settings.grid_height)
        self.state = GameState.MENU
        self.stats = GameStats()
        self._turns_without_infection = 0

    def start_game(self) -> None:
        """Initialize a new game."""
        self.grid.reset()
        self.grid.seed_infections(self.settings.initial_infections)
        self.state = GameState.PLAYING
        self.stats.day = 1
        self.stats.action_points = self.settings.action_points_per_turn
        self._update_stats()
        self._turns_without_infection = 0

    def end_turn(self) -> None:
        """Process one turn: disease spread, recoveries, deaths."""
        if self.state != GameState.PLAYING:
            return

        # Disease spreads
        self.grid.spread_infection(self.settings.infection_rate)

        # Resolve recoveries and deaths
        self.grid.resolve_outcomes(
            recovery_rate=self.settings.recovery_rate,
            mortality_rate=self.settings.mortality_rate,
        )

        # Update stats
        self.stats.day += 1
        self.stats.action_points = self.settings.action_points_per_turn
        self._update_stats()

        # Win condition check
        if self.stats.infected == 0:
            self._turns_without_infection += 1
            if self._turns_without_infection >= self.settings.win_turns_clean:
                self.state = GameState.WON
        else:
            self._turns_without_infection = 0

        # Loss condition check
        if self.stats.dead >= self.settings.population_loss_threshold:
            self.state = GameState.GAMEOVER

    def vaccinate_cell(self, x: int, y: int) -> bool:
        """Vaccinate a cell if player has enough action points."""
        if self.stats.action_points < 2:
            return False
        if self.grid.set_cell_state(x, y, CellState.VACCINATED):
            self.stats.action_points -= 2
            return True
        return False

    def lockdown_cell(self, x: int, y: int) -> bool:
        """Lockdown a cell to prevent spread."""
        if self.stats.action_points < 1:
            return False
        return self.grid.lockdown(x, y)

    def _update_stats(self) -> None:
        counts = self.grid.count_cells()
        self.stats.susceptible = counts.get(CellState.SUSCEPTIBLE, 0)
        self.stats.infected = counts.get(CellState.INFECTED, 0)
        self.stats.recovered = counts.get(CellState.RECOVERED, 0)
        self.stats.dead = counts.get(CellState.DEAD, 0)
        self.stats.vaccinated = counts.get(CellState.VACCINATED, 0)

    def get_state(self) -> GameState:
        return self.state

    def get_stats(self) -> GameStats:
        return self.stats