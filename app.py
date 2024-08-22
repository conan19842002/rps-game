import logging
import os
import random

from flask import Flask, jsonify, render_template, request

from utils import (determine_winner, get_game_key, load_games,
                    save_games_to_file)

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory storage for scores
scores = {"player1": 0, "player2": 0}

# Route to handle game plays
@app.route('/play', methods=['POST'])
def play() -> jsonify:
    """
    Handle the logic for a single round of the game.

    Returns:
        jsonify: JSON response containing the result of the round and updated scores.
    """
    data = request.json
    player1 = data.get("player1", "Player 1")
    player2 = data.get("player2", "Computer")
    player1_move = data.get("player1_move")
    
    if not player1_move:
        return jsonify({"error": "Player 1 move is required"}), 400
    
    # If playing against the computer, randomly select a move for the computer
    player2_move = data.get("player2_move") or random.choice(["rock", "paper", "scissors"])
    
    # Determine the winner
    winner = determine_winner(player1_move, player2_move)
    
    if winner == "player1":
        scores["player1"] += 1
        result = f"{player1} wins!"
    elif winner == "player2":
        scores["player2"] += 1
        result = f"{player2} wins!"
    elif winner == "tie":
        result = "It's a tie!"
    else:
        return jsonify({"error": "Invalid moves"}), 400
    
    logger.info(f"Round result: {result}")
    
    return jsonify({
        "result": result,
        "player1_move": player1_move,
        "player2_move": player2_move,
        "scores": scores
    })

# Route to save the game state
@app.route('/save', methods=['POST'])
def save_game() -> jsonify:
    """
    Save the current game state.

    Returns:
        jsonify: JSON response indicating the success or failure of the save operation.
    """
    data = request.json
    player1_name = data.get('player1_name')
    player2_name = data.get('player2_name')
    player1_score = data.get('player1_score')
    player2_score = data.get('player2_score')

    if not all([player1_name, player2_name, player1_score, player2_score]):
        return jsonify({"error": "All fields are required to save the game"}), 400
    
    game_key = get_game_key(player1_name, player2_name)
    games = load_games()  # Load the current games to include the new one
    games[game_key] = {
        "player1_score": player1_score,
        "player2_score": player2_score
    }
    
    save_games_to_file(games)
    return jsonify({"message": "Game has been saved!"})

# Route to load the game state
@app.route('/load', methods=['POST'])
def load_game() -> jsonify:
    """
    Load a previously saved game state.

    Returns:
        jsonify: JSON response containing the loaded game state or an error message.
    """
    data = request.json
    player1_name = data.get('player1_name')
    player2_name = data.get('player2_name')

    if not player1_name or not player2_name:
        return jsonify({"error": "Player names are required to load the game"}), 400
    
    games = load_games()
    game_key = get_game_key(player1_name, player2_name)
    if game_key in games:
        logger.info(f"Game loaded for players: {player1_name} and {player2_name}")
        return jsonify({
            "message": "Game has been loaded!",
            "scores": {
                "player1": games[game_key]['player1_score'],
                "player2": games[game_key]['player2_score']
            }
        })
    else:
        return jsonify({"message": "No saved game found!"}), 404

# Route to render the main game page
@app.route('/')
def index() -> str:
    """
    Render the main game page.

    Returns:
        str: The HTML content for the main game page.
    """
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', 'false').lower() == 'true')