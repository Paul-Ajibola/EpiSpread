# Epi-Spread — Game Design Document

## Core Concept

A turn-based grid simulation where players respond to an emerging epidemic. Players have limited action points per turn to deploy interventions (vaccines, lockdowns, treatments) while the disease spreads autonomously across the grid.

## Game Loop

1. **State Evaluation** — Check cell states (Susceptible, Infected, Recovered, Dead, Vaccinated)
2. **Player Turn** — Spend action points on interventions
3. **Disease Spread** — Infection propagates to neighboring cells based on probability
4. **Resolution** — Recoveries, deaths, immunity checks
5. **Win/Loss Check** — Disease contained (win) or population overwhelmed (loss)

## Cell States

| State | Description |
|-------|-------------|
| Susceptible | Healthy, can be infected |
| Infected | Currently infected, spreads disease |
| Recovered | Immune, cannot be reinfected |
| Dead | Removed from simulation |
| Vaccinated | Immune via player intervention |

## Player Actions

| Action | Cost | Effect |
|--------|------|--------|
| Vaccinate cell | 2 AP | Makes cell immune |
| Lockdown cell | 1 AP | Blocks spread to/from cell |
| Treat cell | 2 AP | Accelerates recovery |
| Quarantine zone | 3 AP | Locks down 3x3 area |

## Configuration Parameters

- Grid dimensions (default: 20x20)
- Initial infection count
- Base infection rate (probability per neighbor per turn)
- Recovery rate (probability per turn)
- Mortality rate
- Action points per turn
- Win condition (e.g., zero active infections for 5 turns)

## UI

Web-based interface using Flask:
- Grid visualization with color-coded cell states
- Action panel for player interventions
- Status panel (day counter, infection stats, AP remaining)
- Game over / victory screens