"""Tests for the engine module."""

import pytest

from src.core.engine import Engine, GameState
from src.config.settings import Settings


def test_engine_initialization():
    engine = Engine(Settings())
    assert engine.state == GameState.MENU
    assert engine.grid.width == 20


def test_start_game():
    engine = Engine(Settings())
    engine.start_game()
    assert engine.state == GameState.PLAYING
    assert engine.stats.day == 1
    assert engine.stats.infected > 0


def test_end_turn_increments_day():
    engine = Engine(Settings())
    engine.start_game()
    initial_day = engine.stats.day
    engine.end_turn()
    assert engine.stats.day == initial_day + 1


def test_vaccinate_costs_action_points():
    engine = Engine(Settings())
    engine.start_game()
    initial_ap = engine.stats.action_points
    engine.vaccinate_cell(0, 0)
    assert engine.stats.action_points == initial_ap - 2


def test_vaccinate_insufficient_ap():
    engine = Engine(Settings())
    engine.start_game()
    engine.stats.action_points = 1
    result = engine.vaccinate_cell(0, 0)
    assert result is False