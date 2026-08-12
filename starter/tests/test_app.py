"""Tests for the Flask Sudoku app routes."""

import sys
import os

# Ensure the starter/ directory is on the path so we can import app.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app
import sudoku_logic


@pytest.fixture
def client():
    """Provides a Flask test client for making requests."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index_route(client):
    """The home page should load successfully."""
    response = client.get('/')
    assert response.status_code == 200


def test_new_game_route(client):
    """Starting a new game should return a puzzle with the correct structure."""
    response = client.get('/new')
    assert response.status_code == 200

    data = response.get_json()
    assert 'puzzle' in data

    puzzle = data['puzzle']
    assert len(puzzle) == sudoku_logic.SIZE
    for row in puzzle:
        assert len(row) == sudoku_logic.SIZE


def test_check_route_no_game_in_progress(client):
    """Calling /check with no active game should return a 400 error."""
    # Reset any existing game state
    from app import CURRENT
    CURRENT['puzzle'] = None
    CURRENT['solution'] = None

    response = client.post('/check', json={'board': [[0] * 9 for _ in range(9)]})
    assert response.status_code == 400


def test_check_route_identifies_incorrect_cells(client):
    """Calling /check should correctly identify incorrect cells."""
    # Start a new game first so a solution exists
    client.get('/new')

    # Submit an all-zero board, which will almost certainly be wrong everywhere
    # a real number belongs in the solution
    wrong_board = [[0] * sudoku_logic.SIZE for _ in range(sudoku_logic.SIZE)]

    response = client.post('/check', json={'board': wrong_board})
    assert response.status_code == 200

    data = response.get_json()
    assert 'incorrect' in data
    assert isinstance(data['incorrect'], list)
    assert len(data['incorrect']) > 0