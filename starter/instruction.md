# Project Instructions for GitHub Copilot

## Overview
This is a Flask-based Sudoku web app, refactored from legacy code into a modular,
well-tested application with difficulty levels, hints, a timer, a top-10 leaderboard,
and light/dark mode support.

## Coding Style & Conventions
- Follow PEP 8 for all Python code.
- Use descriptive, snake_case names for functions and variables (e.g. `generate_puzzle`,
  `is_valid_move`), and PascalCase for classes.
- Every function should have a docstring explaining its purpose, parameters, and return value.
- Keep functions small and single-purpose. If a function is doing more than one thing,
  split it up.
- Avoid global mutable state where possible (e.g. the legacy `CURRENT` dict in app.py
  should be replaced with proper session-based or per-game state).

## Project Structure
Organize the app into clear, modular components:
- `app.py` — Flask routes only. No game logic here.
- `sudoku_logic.py` — puzzle generation logic.
- `solver.py` — Sudoku solving and unique-solution validation.
- `game.py` — game state management (current puzzle, timer, hints used, etc.).
- `templates/` — HTML templates.
- `static/js/` — frontend JavaScript, split by concern (e.g. `board.js`, `timer.js`,
  `leaderboard.js`).
- `static/css/` — stylesheets.
- `tests/` — pytest test files, mirroring the module structure (e.g. `test_solver.py`).

## Error Handling
- All Flask routes should validate input and return clear JSON error messages with
  appropriate HTTP status codes (e.g. 400 for bad input, 404 for not found).
- Never let an unhandled exception crash a route — wrap risky logic in try/except and
  return a meaningful error response.
- Log errors server-side for debugging.

## Testing
- Use `pytest` as the testing framework.
- Every new feature or refactored function should have at least one corresponding test.
- Tests live in the `tests/` folder and mirror the structure of the app.
- Run tests with: `pytest`
- Tests must pass before a feature is considered complete.

## Comments
- Comment non-obvious logic (e.g. why a particular algorithm was chosen for solving
  or validating uniqueness), not obvious code.
- Prefer clear code over excessive comments, but never leave complex logic unexplained.

## Frontend Conventions
- Use vanilla JavaScript and plain CSS (no framework) for simplicity and to keep the
  project lightweight.
- Keep JS organized by feature/concern in separate files.
- CSS should support both light and dark mode via a toggleable class or CSS variables.
- Layout must be responsive (mobile and desktop) using flexbox/grid and media queries.

## Copilot Usage Guidelines
- When Copilot suggests code, review it critically before accepting — don't accept
  blindly.
- Prefer clear, working code over clever one-liners.
- If a suggestion overcomplicates something or doesn't fit the existing structure,
  reject it and either revise the prompt or write it manually.