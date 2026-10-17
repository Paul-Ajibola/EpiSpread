"""Grid logic, cell states, and neighbor evaluation."""

from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class CellState(Enum):
    SUSCEPTIBLE = auto()
    INFECTED = auto()
    RECOVERED = auto()
    DEAD = auto()
    VACCINATED = auto()


@dataclass
class Cell:
    x: int
    y: int
    state: CellState = CellState.SUSCEPTIBLE
    locked_down: bool = False
    days_infected: int = 0


class Grid:
    """A 2D grid of cells representing the simulation space."""

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self._cells: dict[tuple[int, int], Cell] = {}
        for x in range(width):
            for y in range(height):
                self._cells[(x, y)] = Cell(x, y)

    def reset(self) -> None:
        """Reset all cells to susceptible state."""
        for cell in self._cells.values():
            cell.state = CellState.SUSCEPTIBLE
            cell.locked_down = False
            cell.days_infected = 0

    def seed_infections(self, count: int) -> None:
        """Randomly infect a number of cells."""
        positions = random.sample(list(self._cells.keys()), min(count, len(self._cells)))
        for x, y in positions:
            self._cells[(x, y)].state = CellState.INFECTED

    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        return self._cells.get((x, y))

    def set_cell_state(self, x: int, y: int, state: CellState) -> bool:
        cell = self.get_cell(x, y)
        if cell is None:
            return False
        cell.state = state
        return True

    def lockdown(self, x: int, y: int) -> bool:
        cell = self.get_cell(x, y)
        if cell is None:
            return False
        cell.locked_down = True
        return True

    def get_neighbors(self, x: int, y: int) -> list[Cell]:
        """Get all 8 neighboring cells (Moore neighborhood)."""
        neighbors = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbors.append(self._cells[(nx, ny)])
        return neighbors

    def spread_infection(self, infection_rate: float) -> list[tuple[int, int]]:
        """Spread infection from infected cells to susceptible neighbors."""
        newly_infected: list[tuple[int, int]] = []
        for (x, y), cell in self._cells.items():
            if cell.state != CellState.INFECTED or cell.locked_down:
                continue
            for neighbor in self.get_neighbors(x, y):
                if (
                    neighbor.state == CellState.SUSCEPTIBLE
                    and not neighbor.locked_down
                    and random.random() < infection_rate
                ):
                    neighbor.state = CellState.INFECTED
                    newly_infected.append((neighbor.x, neighbor.y))
        return newly_infected

    def resolve_outcomes(
        self,
        recovery_rate: float,
        mortality_rate: float,
    ) -> None:
        """Process recoveries and deaths for infected cells."""
        for cell in self._cells.values():
            if cell.state != CellState.INFECTED:
                continue
            cell.days_infected += 1
            roll = random.random()
            if roll < mortality_rate:
                cell.state = CellState.DEAD
            elif roll < mortality_rate + recovery_rate:
                cell.state = CellState.RECOVERED

    def count_cells(self) -> dict[CellState, int]:
        counts: dict[CellState, int] = {state: 0 for state in CellState}
        for cell in self._cells.values():
            counts[cell.state] += 1
        return counts