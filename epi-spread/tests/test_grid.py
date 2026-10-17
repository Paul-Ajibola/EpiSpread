"""Tests for the grid module."""

import pytest

from src.core.grid import Grid, CellState


def test_grid_initialization():
    grid = Grid(10, 10)
    assert grid.width == 10
    assert grid.height == 10
    assert len(grid._cells) == 100


def test_all_cells_susceptible_after_reset():
    grid = Grid(5, 5)
    grid.reset()
    for cell in grid._cells.values():
        assert cell.state == CellState.SUSCEPTIBLE


def test_seed_infections():
    grid = Grid(10, 10)
    grid.reset()
    grid.seed_infections(5)
    infected_count = sum(
        1 for c in grid._cells.values() if c.state == CellState.INFECTED
    )
    assert infected_count == 5


def test_set_cell_state():
    grid = Grid(5, 5)
    assert grid.set_cell_state(0, 0, CellState.INFECTED)
    assert grid.get_cell(0, 0).state == CellState.INFECTED
    assert not grid.set_cell_state(99, 99, CellState.INFECTED)


def test_get_neighbors():
    grid = Grid(5, 5)
    neighbors = grid.get_neighbors(0, 0)
    assert len(neighbors) == 3
    neighbors = grid.get_neighbors(2, 2)
    assert len(neighbors) == 8


def test_spread_infection():
    grid = Grid(5, 5)
    grid.reset()
    grid.set_cell_state(2, 2, CellState.INFECTED)
    grid.spread_infection(1.0)
    neighbors = grid.get_neighbors(2, 2)
    infected_neighbors = sum(
        1 for n in neighbors if n.state == CellState.INFECTED
    )
    assert infected_neighbors == 8


def test_count_cells():
    grid = Grid(3, 3)
    grid.reset()
    grid.set_cell_state(0, 0, CellState.INFECTED)
    grid.set_cell_state(1, 1, CellState.VACCINATED)
    counts = grid.count_cells()
    assert counts[CellState.SUSCEPTIBLE] == 7
    assert counts[CellState.INFECTED] == 1
    assert counts[CellState.VACCINATED] == 1