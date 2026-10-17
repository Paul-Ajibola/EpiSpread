# Epi-Spread — Agent Instructions

This file provides guidance for AI agents working on the Epi-Spread project.

## Project Overview

Epi-Spread is a Python-based grid simulation game where players manage disease containment on a cellular grid. The project follows a modular structure:

- `src/core/engine.py` — Main simulation loop and game state machine
- `src/core/grid.py` — Grid logic, cell states, neighbor evaluation
- `src/config/settings.py` — Grid dimensions, infection rates, action points
- `src/ui/web_app.py` — Frontend interface / rendering script
- `tests/` — Unit tests for engine and grid

## Coding Conventions

- Language: Python 3.9+
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Docstrings for all public classes and methods
- Unit tests for all core logic

## Key Systems

### Grid System
- Cells can be in states: Susceptible, Infected, Recovered, Dead, Vaccinated
- Neighbor evaluation uses Moore neighborhood (8 surrounding cells)
- Infection spreads probabilistically based on infection rate

### Engine
- Turn-based simulation loop
- Action point system for player interventions
- Game state machine: Menu → Playing → Paused → GameOver → Won

### Configuration
- All tunable parameters live in `src/config/settings.py`
- Grid dimensions, infection rates, recovery rates, action points per turn

## Testing

Run tests with: `pytest`
Aim for >80% code coverage on core modules.

## Commit Convention

Use conventional commits: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`