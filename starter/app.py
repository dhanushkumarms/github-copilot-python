from flask import Flask, render_template, jsonify, request, session
import random
import sudoku_logic

app = Flask(__name__)
app.secret_key = 'dev-secret-key-change-this-in-production'  # required for sessions

# Maps difficulty names to number of prefilled clues
DIFFICULTY_CLUES = {
    'easy': 45,
    'medium': 35,
    'hard': 25
}


@app.route('/')
def index():
    """Render the main game page."""
    return render_template('index.html')


@app.route('/new')
def new_game():
    """Start a new game. Accepts a 'difficulty' query param (easy/medium/hard)."""
    difficulty = request.args.get('difficulty', 'medium').lower()
    clues = DIFFICULTY_CLUES.get(difficulty, DIFFICULTY_CLUES['medium'])

    puzzle, solution = sudoku_logic.generate_puzzle(clues)

    # Store this player's game in their own session, not a shared global dict
    session['puzzle'] = puzzle
    session['solution'] = solution
    session['difficulty'] = difficulty
    session['hints_used'] = 0

    return jsonify({'puzzle': puzzle, 'difficulty': difficulty})


@app.route('/check', methods=['POST'])
def check_solution():
    """Compare the submitted board against this player's stored solution."""
    data = request.json
    board = data.get('board')
    solution = session.get('solution')

    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400

    incorrect = []
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])

    return jsonify({'incorrect': incorrect})


@app.route('/hint', methods=['POST'])
def get_hint():
    """Return one correct, currently-empty cell and its value, and lock it."""
    data = request.json
    board = data.get('board')
    solution = session.get('solution')

    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400

    empty_cells = [
        (i, j)
        for i in range(sudoku_logic.SIZE)
        for j in range(sudoku_logic.SIZE)
        if board[i][j] == 0
    ]

    if not empty_cells:
        return jsonify({'error': 'No empty cells left'}), 400

    row, col = random.choice(empty_cells)
    value = solution[row][col]

    session['hints_used'] = session.get('hints_used', 0) + 1

    return jsonify({
        'row': row,
        'col': col,
        'value': value,
        'hints_used': session['hints_used']
    })


if __name__ == '__main__':
    app.run(debug=True)