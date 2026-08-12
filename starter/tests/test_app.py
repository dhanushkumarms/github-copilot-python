"""Tests for the Flask Sudoku app routes."""

import sys
import os

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
    assert 'difficulty' in data

    puzzle = data['puzzle']
    assert len(puzzle) == sudoku_logic.SIZE
    for row in puzzle:
        assert len(row) == sudoku_logic.SIZE


def test_new_game_difficulty_affects_clue_count(client):
    """Different difficulties should produce different numbers of prefilled cells."""
    easy_response = client.get('/new?difficulty=easy')
    easy_puzzle = easy_response.get_json()['puzzle']
    easy_clues = sum(1 for row in easy_puzzle for cell in row if cell != 0)

    hard_response = client.get('/new?difficulty=hard')
    hard_puzzle = hard_response.get_json()['puzzle']
    hard_clues = sum(1 for row in hard_puzzle for cell in row if cell != 0)

    assert easy_clues > hard_clues


def test_check_route_no_game_in_progress(client):
    """Calling /check with no active game (fresh session) should return a 400 error."""
    response = client.post('/check', json={'board': [[0] * 9 for _ in range(9)]})
    assert response.status_code == 400


def test_check_route_identifies_incorrect_cells(client):
    """Calling /check should correctly identify incorrect cells."""
    client.get('/new')  # start a new game so a solution exists in the session

    wrong_board = [[0] * sudoku_logic.SIZE for _ in range(sudoku_logic.SIZE)]

    response = client.post('/check', json={'board': wrong_board})
    assert response.status_code == 200

    data = response.get_json()
    assert 'incorrect' in data
    assert isinstance(data['incorrect'], list)
    assert len(data['incorrect']) > 0


def test_hint_route_fills_valid_cell(client):
    """Calling /hint should return a valid cell and value, and increment hints_used."""
    new_game_response = client.get('/new')
    puzzle = new_game_response.get_json()['puzzle']

    response = client.post('/hint', json={'board': puzzle})
    assert response.status_code == 200

    data = response.get_json()
    assert 'row' in data
    assert 'col' in data
    assert 'value' in data
    assert 1 <= data['value'] <= 9
    assert data['hints_used'] == 1


def test_hint_route_no_game_in_progress(client):
    """Calling /hint with no active game should return a 400 error."""
    response = client.post('/hint', json={'board': [[0] * 9 for _ in range(9)]})
    assert response.status_code == 400